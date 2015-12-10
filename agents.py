import random
import eval

class ExpectimaxAgent():
	def __init__(self):
		self.depth = 2

	def evaluationFunction(self, gameState):
		return eval.eval_snake(gameState.board)

	def getAction(self, gameState, index, validActions):
		# Return (minimax value Vopt(state), random number, optimal action pi_opt(state))
		def recurse(gameState, index, depth):
			if gameState.isWin() or gameState.isLose():
				return gameState.getScore(), random.random(), None
			if depth == 0:
				return self.evaluationFunction(gameState), random.random(), None

			if index == 0: # human
				return max([(recurse(gameState.generateSuccessor(index, action), 1, depth)[0], random.random(), action) for action in gameState.getLegalActions(index, validActions)])
			elif index == 1: # computer
				return sum([recurse(gameState.generateSuccessor(index, action), 0, depth - 1)[0] for action in gameState.getLegalActions(index, validActions)]) / len(gameState.getLegalActions(index, validActions)), random.random(), random.choice(gameState.getLegalActions(index, validActions))
		utility, rand, action = recurse(gameState, index, self.depth)
		return action

	def getComputerAction(self, gameState, validActions):
		print 1
		return random.choice(gameState.getLegalActions(1, validActions))

class MinimaxAgent():
	def __init__(self):
		self.depth = 3

	def evaluationFunction(self, gameState):
		return eval.eval_snake(gameState.board)

	def getAction(self, gameState, index, validActions):
		# Return (minimax value Vopt(state), random number, optimal action pi_opt(state))
		def recurse(gameState, index, depth):
			if gameState.isWin() or gameState.isLose():
				return gameState.getScore(), random.random(), None
			if depth == 0:
				return self.evaluationFunction(gameState), random.random(), None

			if index == 0: # humam
				return max([(recurse(gameState.generateSuccessor(index, action), 1, depth)[0], random.random(), action) for action in gameState.getLegalActions(index, validActions)])
			elif index == 1: # computer
				return min([(recurse(gameState.generateSuccessor(index, action), 0, depth - 1)[0], random.random(), action) for action in gameState.getLegalActions(index, validActions)])
		utility, rand, action = recurse(gameState, index, self.depth)
		return action

class AlphaBetaAgent():
	def __init__(self):
		self.depth = 3

	def evaluationFunction(self, gameState):
		return eval.eval_monotonicity(gameState.board)

	def getAction(self, gameState, index, validActions):

		def recurse(gameState, index, depth, alpha, beta):
			if gameState.isWin() or gameState.isLose():
				return gameState.getScore(), random.random(), None
			if depth == 0:
				return self.evaluationFunction(gameState), random.random(), None
			if index == 0: # human
				maximum = (float('-inf'), random.random(), None)
				for action in gameState.getLegalActions(index, validActions):
					maximum = max(maximum, (recurse(gameState.generateSuccessor(index, action), 1, depth, alpha, beta)[0], random.random(), action))
					alpha = max(alpha, maximum[0]) # maximum[0] is the max utility
					if beta <= alpha:
						break
				return maximum
			elif index == 1: # computer
				minimum = (float('inf'), random.random(), None)
				for action in gameState.getLegalActions(index, validActions):
					minimum = min(minimum, (recurse(gameState.generateSuccessor(index, action), 0, depth - 1, alpha, beta)[0], random.random(), action))
					beta = min(beta, minimum[0]) # minimum[0] is the min utility
					if beta <= alpha:
						break
				return minimum

		utility, rand, action = recurse(gameState, index, self.depth, float('-inf'), float('inf'))
		return action