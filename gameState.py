class Move:
	left, up, right, down = range(4)

	def getAllMoves(self):
		return [self.left, self.up, self.right, self.down]

class GameState2048:
	"""
	A GameState2048 specifies the full game state, including the tile values,
	scores, and more.
	"""

	BOARD_SIZE = 4
	WINNING_TILE = 2048

	def __init__(self):
		self.board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)] # store the value at each tile, 0 means empty
		self.score = 0
		self.moves = Move()

	def getLegalAction(self, agentIndex = 0):
		assert agentIndex == 0 or agentIndex == 1
		if self.isWin() or self.isLose():
			return []
		if agentIndex == 0:  # human player
		  return self.moves.getAllMoves()
		else:
		  return [(row, col) for col in range(self.BOARD_SIZE) for row in range(self.BOARD_SIZE) if self.isTileEmpty(row, col)]

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

game = GameState2048()

assert game.board == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

assert game.getLegalAction(0) == [game.moves.left, game.moves.up, game.moves.right, game.moves.down]
assert len(game.getLegalAction(1)) == game.BOARD_SIZE ** 2

assert game.isLose() == False
game.setValue(0, 0, game.WINNING_TILE)
assert game.isWin() == True