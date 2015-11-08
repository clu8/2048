class GameState2048:
	"""
	A GameState2048 specifies the full game state, including the tile values,
	scores, and more.
	"""

	def __init__(self, size):
		self.board = [[0 for _ in range(size)] for _ in range(size)]

game = GameState2048(4)
assert game.board == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]