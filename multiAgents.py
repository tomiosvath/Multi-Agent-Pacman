# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class RandomAgent(Agent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        # Pick randomly among the legal
        chosenIndex = random.choice(range(0, len(legalMoves)))
        return legalMoves[chosenIndex]


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        distToFood = [manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]
        distToGhosts = [manhattanDistance(newPos, gP) for gP in currentGameState.getGhostPositions()]

        d1 = min(distToFood) if len(distToFood) > 0 else 0
        d2 = min(distToGhosts) if len(distToGhosts) > 0 else 0

        return successorGameState.getScore() - d1 + d2

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        return self.minimax(gameState, self.depth)[1]

    def minimax(self, gameState, depth, agent=0): #minimax[0] returns a score, [1] actions
        if gameState.isLose() or gameState.isWin() or depth < 1:
            return self.evaluationFunction(gameState),

        tmpDepth = depth
        tmpAgent = 0 #0 means the pacMan, the rest are ghosts
        if agent + 1 == gameState.getNumAgents(): #if the agent is the last one
            tmpDepth -= 1
        else:
            tmpAgent = agent + 1

        actions = [(self.minimax(gameState.generateSuccessor(agent, i), tmpDepth, tmpAgent)[0], i) for i in gameState.getLegalActions(agent)]
        if agent:
            return min(actions)

        return max(actions)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        def maxValue(state, depth, agent, a, b):
            v = float("-inf")
            for successor in state.getLegalActions(agent):
                v = max(v, value(state.generateSuccessor(agent, successor), depth, 1, a, b))
                if v > b:
                    return v
                a = max(a, v)
            return v

        def minValue(state, depth, agent, a, b):
            tmpAgent = agent + 1
            tmpDepth = depth
            v = float("inf")
            if state.getNumAgents() == agent + 1:
                tmpAgent = 0
                tmpDepth += 1

            for successor in state.getLegalActions(agent):
                v = min(v, value(state.generateSuccessor(agent, successor), tmpDepth, tmpAgent, a, b))
                if v < a:
                    return v
                b = min(b, v)
            return v

        def value(state, depth, agent, a, b):
            if state.isLose() or state.isWin() or depth == self.depth:
                return self.evaluationFunction(state)
            if agent:
                return minValue(state, depth, agent, a, b)
            return maxValue(state, depth, agent, a, b)

        action = []
        score = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        for agentState in gameState.getLegalActions(0):
            v = value(gameState.generateSuccessor(0, agentState), 0, 1, alpha, beta)
            if v > score:
                score = v
                action = agentState
            alpha = max(alpha, score)

        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

