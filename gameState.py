import random

class Move:
	left, up, right, down = range(4)

	def getAllMoves(self):
		return [self.left, self.up, self.right, self.down]

	def moveString(self, move):
		if move == self.left:
			return 'left'
		elif move == self.up:
			return 'up'
		elif move == self.right:
			return 'right'
		elif move == self.down:
			return 'down'

class GameState2048:
	"""
	A GameState2048 specifies the full game state, including the tile values,
	scores, and more.
	"""

	BOARD_SIZE = 4
	WINNING_TILE = 2048

	def __init__(self, prevState = None):
		if prevState:
			self.board = [[prevState.board[row][col] for col in range(self.BOARD_SIZE)] for row in range(self.BOARD_SIZE)] # store the value at each tile, 0 means empty
			self.score = prevState.score
		else:
			self.board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)] # store the value at each tile, 0 means empty
			self.score = 0
		self.moves = Move()

	def getLegalActions(self, agentIndex = 0):
		assert agentIndex == 0 or agentIndex == 1
		if self.isWin() or self.isLose():
			return []
		if agentIndex == 0:	# human player
			return self.moves.getAllMoves()
		else:
			return [(row, col) for col in range(self.BOARD_SIZE) for row in range(self.BOARD_SIZE) if self.isTileEmpty(row, col)]

	def collapse(self, values):
		collapsed = list(filter(lambda x: x != 0, values))
		i = len(collapsed) - 1
		while i > 0:
			if collapsed[i] == collapsed[i - 1]:
				collapsed[i] *= 2
				self.score += collapsed[i]
				collapsed.pop(i - 1)
				i -= 1
			i -= 1
		return [0] * (len(values) - len(collapsed)) + collapsed

	def generateSuccessor(self, agentIndex, action):
		# Check that successors exist
		if self.isWin() or self.isLose():
			raise Exception('Can\'t generate a successor of a terminal state.')

		# Copy current state
		state = GameState2048(self)

		if agentIndex == 0: # human player
			if action == self.moves.left:
				state.board = [state.collapse(row[::-1])[::-1] for row in state.board]
			elif action == self.moves.up:
				transposed = zip(*state.board)
				collapsed = [state.collapse(col[::-1])[::-1] for col in transposed]
				state.board = list(map(lambda x: list(x), zip(*collapsed)))
			elif action == self.moves.right:
				state.board = [state.collapse(row) for row in state.board]
			elif action == self.moves.down:
				transposed = zip(*state.board)
				collapsed = [state.collapse(col) for col in transposed]
				state.board = list(map(lambda x: list(x), zip(*collapsed)))
		else:
			row, col = action
			state.board[row][col] = 2 # should we allow 4?

		return state

	def isWin(self):
		for row in self.board:
			for tile in row:
				if tile == self.WINNING_TILE:
					return True
		return False

	def isLose(self):
		for row in self.board:
			for tile in row:
				if tile == 0:
					return False
		return True

	def isTileEmpty(self, row, col):
		return self.board[row][col] == 0

	def setValue(self, row, col, value):
		assert value ^ (value - 1) # value should be power of 2
		self.board[row][col] = value

	@staticmethod
	def printBoard(board):
		text = ''
		for row in board:
			for tile in row:
				text += str(tile) + ' '
			text += '\n'
		print text.strip('\n')

# game = GameState2048()

# assert game.board == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

# assert game.getLegalActions(0) == [game.moves.left, game.moves.up, game.moves.right, game.moves.down]
# assert len(game.getLegalActions(1)) == game.BOARD_SIZE ** 2

# assert game.isLose() == False
# game.setValue(0, 0, game.WINNING_TILE)
# assert game.isWin() == True

# game.board = [[2, 2, 0, 0], [4, 2, 8, 0], [0, 2, 0, 0], [0, 2, 0, 0]]
# game.printBoard(game.board)

# for move in game.getLegalActions(0):
# 	newState = game.generateSuccessor(0, move)
# 	print '\nScore', newState.score
# 	game.printBoard(newState.board)

class ExpectimaxAgent():
	
	def __init__(self):
		self.depth = 3

	def evaluationFunction(self, gameState):
		return gameState.score

	def getAction(self, gameState, index):
		# Return (minimax value Vopt(state), random number, optimal action pi_opt(state))
		def recurse(gameState, index, depth):
			if gameState.isWin() or gameState.isLose():
				return gameState.getScore(), random.random(), None
			if depth == 0:
				return self.evaluationFunction(gameState), random.random(), None

			if index == 0: # human
				return max([(recurse(gameState.generateSuccessor(index, action), 1, depth)[0], random.random(), action) for action in gameState.getLegalActions(index)])
			elif index == 1: # computer
				return sum([recurse(gameState.generateSuccessor(index, action), 0, depth - 1)[0] for action in gameState.getLegalActions(index)]) / len(gameState.getLegalActions(index)), random.random(), random.choice(gameState.getLegalActions(index))
		utility, rand, action = recurse(gameState, index, self.depth)
		return action

class MinimaxAgent():
	
	def __init__(self):
		self.depth = 3

	def evaluationFunction(self, gameState):
		return gameState.score

	def getAction(self, gameState, index):
		# Return (minimax value Vopt(state), random number, optimal action pi_opt(state))
		def recurse(gameState, index, depth):
			if gameState.isWin() or gameState.isLose():
				return gameState.getScore(), random.random(), None
			if depth == 0:
				return self.evaluationFunction(gameState), random.random(), None

			if index == 0: # humam
				return max([(recurse(gameState.generateSuccessor(index, action), 1, depth)[0], random.random(), action) for action in gameState.getLegalActions(index)])
			elif index == 1: # computer
				return min([(recurse(gameState.generateSuccessor(index, action), 0, depth - 1)[0], random.random(), action) for action in gameState.getLegalActions(index)])
		utility, rand, action = recurse(gameState, index, self.depth)
		return action

move = Move()
gameState = GameState2048()
gameState.board = [[2, 2, 0, 0], [4, 2, 8, 0], [0, 2, 0, 0], [0, 2, 0, 0]]
agent = ExpectimaxAgent()

for _ in range(10):
	gameState.printBoard(gameState.board)
	humanAction = agent.getAction(gameState, 0)
	print 'human move: ' + move.moveString(humanAction)
	gameState = gameState.generateSuccessor(0, humanAction)
	computerAction = agent.getAction(gameState, 1)
	print 'computer move: ' + str(computerAction)
	gameState = gameState.generateSuccessor(1, computerAction)