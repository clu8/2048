from enum import Enum

class Move(Enum):
    left = 1
    up = 2
    right = 3
    down = 4

    def getAllMoves():
    	return [left, up, right, down]

class GameState2048:
	"""
	A GameState2048 specifies the full game state, including the tile values,
	scores, and more.
	"""

	BOARD_SIZE = 4
	WINNING_TILE = 2048

	def __init__(self):
		self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)] # store the value at each tile, 0 means empty
		self.score = 0

	def getLegalAction(self, agentIndex = 0):
		assert agentIndex == 0 or agentIndex == 1
		if self.isWin() or self.isLose():
			return []
		if agentIndex == 0:  # human player
		  return Move.getAllMoves()
		else:
		  return [(row, col) for col in range(BOARD_SIZE) for row in range(BOARD_SIZE) if self.isTileEmpty(row, col)]

	def isWin(self):
		for row in self.board:
			for tile in row:
				if tile == WINNING_TILE:
					return True
		return False

	def isLose(self):
		for row in self.board:
			for tile in row:
				if tile == 0:
					return False
		return True

	def isTileEmpty(row, col):
		return self.board[row][col] == 0

	def setValue(row, col, value):
		assert value ^ (value - 1) # value should be power of 2
		self.board[row][col] = value

game = GameState2048()

assert game.board == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

assert game.getLegalAction(0) == [Move.left, Move.up, Move.right, Move.down]

row, col = game.getLegalAction(1)
assert row >= 0 and row < game.BOARD_SIZE
assert col >= 0 and col < game.BOARD_SIZE

assert game.isWin() == False
assert game.isLose() == False