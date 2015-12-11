import random
import agents

class Move:
    up, right, down, left = list(range(4))

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

    def __init__(self, prevState=None):
        if prevState:
            self.board = [[prevState.board[row][col] for col in range(self.BOARD_SIZE)] for row in range(self.BOARD_SIZE)] # store the value at each tile, 0 means empty
            self.score = prevState.score
        else:
            self.board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)] # store the value at each tile, 0 means empty
            self.score = 0
        self.moves = Move()

    def getLegalActions(self, agentIndex=0, validActions=None):
        assert agentIndex == 0 or agentIndex == 1
        if self.isLose():
            return []
        if agentIndex == 0: # human player
            return self.moves.getAllMoves() if not validActions else validActions
        else:
            return [(row, col) for col in range(self.BOARD_SIZE) for row in range(self.BOARD_SIZE) if self.isTileEmpty(row, col)]

    def collapse(self, values):
        collapsed = list([x for x in values if x != 0])
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
        if self.isLose():
            raise Exception('Can\'t generate a successor of a terminal state.')

        # Copy current state
        state = GameState2048(self)

        if agentIndex == 0: # human player
            if action == self.moves.left:
                state.board = [state.collapse(row[::-1])[::-1] for row in state.board]
            elif action == self.moves.up:
                transposed = list(zip(*state.board))
                collapsed = [state.collapse(col[::-1])[::-1] for col in transposed]
                state.board = list([list(x) for x in zip(*collapsed)])
            elif action == self.moves.right:
                state.board = [state.collapse(row) for row in state.board]
            elif action == self.moves.down:
                transposed = list(zip(*state.board))
                collapsed = [state.collapse(col) for col in transposed]
                state.board = list([list(x) for x in zip(*collapsed)])
        else:
            row, col = action
            state.board[row][col] = 2 # should we allow 4?

        return state

    def checkForTile(self, tileValue=2048):
        for row in self.board:
            for tile in row:
                if tile == tileValue:
                    return True
        return False

    def isLose(self):
        for row in self.board:
            for tile in row:
                if tile == 0:
                    return False
        return True

    def getScore(self):
        return self.score

    def isTileEmpty(self, row, col):
        return self.board[row][col] == 0

    def setValue(self, row, col, value):
        assert value ^ (value - 1) # value should be power of 2
        self.board[row][col] = value

    def __str__(self):
        def serialize(value):
            s = '.' if value == 0 else str(value)
            return '{:4}'.format(s)

        return 'Score: {}\n'.format(self.score) + \
            '\n'.join([' '.join([serialize(self.board[r][c]) for c in range(self.BOARD_SIZE)]) 
                       for r in range(self.BOARD_SIZE)])

# game = GameState2048()

# assert game.board == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

# assert game.getLegalActions(0) == [game.moves.left, game.moves.up,
# game.moves.right, game.moves.down]
# assert len(game.getLegalActions(1)) == game.BOARD_SIZE ** 2

# assert game.isLose() == False
# game.setValue(0, 0, game.WINNING_TILE)
# assert game.isWin() == True

# game.board = [[2, 2, 0, 0], [4, 2, 8, 0], [0, 2, 0, 0], [0, 2, 0, 0]]

# for move in game.getLegalActions(0):
#   newState = game.generateSuccessor(0, move)
#   print '\nScore', newState.score
def run(board, score):
    move = Move()
    gameState = GameState2048()
    gameState.board = board
    gameState.score = score
    agent = agents.AlphaBetaAgent()
    validActions = move.getAllMoves()
    while True:
        humanAction = agent.getAction(gameState, 0, validActions)
        if humanAction is None:
            return None
        newGameState = gameState.generateSuccessor(0, humanAction)
        if gameState.board != newGameState.board:
            return humanAction
        else:
            validActions.remove(humanAction)

def simulate(num_games=1, verbose=False):
    '''
    Returns list of (score, num_moves) tuples.
    '''
    results = []

    move = Move()
    agent = agents.ExpectimaxAgent()
    validActions = move.getAllMoves()

    for i in range(num_games):
        gameState = GameState2048()
        num_moves = 0
        while True:
            num_moves += 1

            computerAction = agent.getAction(gameState, 1, None)
            if computerAction is None:
                break
            gameState = gameState.generateSuccessor(1, computerAction)

            if verbose:
                print(gameState)
            humanAction = move.getAllMoves()[int(raw_input())]
            if humanAction is None:
                break
            else:
                print('Agent move: {}\n'.format(move.moveString(humanAction)))
            gameState = gameState.generateSuccessor(0, humanAction)

        print(gameState)
        results.append((gameState.score, num_moves))

    return results

if __name__ == '__main__':
    print(simulate(5, True))