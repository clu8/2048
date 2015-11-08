class GameState2048:
	"""
	A GameState2048 specifies the full game state, including the tile values,
	scores, and more.
	"""

	WINNING_TILE = 2048

	def __init__(self, size):
		self.board = [[0 for _ in range(size)] for _ in range(size)] # store the value at each tile, 0 means empty
		self.score = 0

	def isWin():
		for row in self.board:
			for tile in row:
				if tile == 2048:
					return True
		return False

	def isLose():
		for row in self.board:
			for tile in row:
				if tile > 0:
					return False
		return True

game = GameState2048(4)
assert game.board == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]