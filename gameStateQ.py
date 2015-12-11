import random
import agents
from subprocess import Popen, PIPE, STDOUT
import time
import json
import sys

last_score = 0
ind = 0
p = Popen(['th', 'gameStateQ.lua'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
score_record = []
max_score = 0


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
        self.won = False
        row = random.randrange(4)
        col = random.randrange(4)
        self.board[row][col] = 2 if random.random() < 0.9 else 4

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
            # raise Exception('Can\'t generate a successor of a terminal state.')
            return None

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
            state.board[row][col] = 2 if random.random() < 0.9 else 4

        for row in self.board:
            for grid in row:
                if grid >= 2048:
                    self.won = True
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

def getComputerAction(gameState, validActions):
    actions = gameState.getLegalActions(1, validActions)
    return None if len(actions) == 0 else random.choice(actions)


def move(gameState):
    
    global last_score
    global ind
    global f
    global score_record
    global max_score

    ### Book keeping of score
    new_score = gameState.score
    print "score", new_score
    if new_score > max_score:
        max_score = new_score
    score_record.append(new_score)
    if len(score_record) == 10240:
        f = open('qlearning/trainingRecord.csv', 'a')
        f.write(str((float(sum(score_record))/(len(score_record)))) + "\n")
        f.close()
        score_record = []
    new_won = gameState.won
    reward = 0
    if new_won:
        reward = 100000
    if (new_score < last_score):
        # print "record", new_score
        # f.write(str(last_score) + "\n")
        if not new_won:
            reward = -2000
    else:
        if not new_won:
            reward = new_score - last_score
    last_score = new_score
    print "reward", reward

    ### Input to lua process
    # print "layout", gameState.board
    layoutStr = gridToStr(gameState.board, reward)
    # print "input", layoutStr
    p.stdin.write(layoutStr)

    qOutput = p.stdout.readline()
    # print "output", qOutput
    print "index", str(ind)

    ### Feed move into front-end
    # data = {'move': int(qOutput),}
    # resp = Response(json.dumps(data), status=200, mimetype='application/json')

    # Keep track of number of moves
    ind += 1
    return int(qOutput)                     # 0: Up, 1: Right, 2: Down, 3: Left
    
    """
    global ind
    ind += 1
    print "index", str(ind)
    p.stdin.write("2 2 0 0 4 2 8 0 0 2 0 0 0 2 0 0 -50 0\n")
    return int(p.stdout.readline())
    """

def gridToStr(layout, reward):
    global max_score
    gridStr = ""
    for row in layout:
        for num in row:
            gridStr += str(num) + " "
    return gridStr + str(reward) + " " +  str(max_score) + " \n"


if __name__ == '__main__':
    validActions = Move().getAllMoves()
    gameState = GameState2048()
    agent = agents.ExpectimaxAgent()
    lastState = gameState
    while True:
        time.sleep(1)
        if lastState.board != gameState.board:
            computerAction = getComputerAction(gameState, None)
            if computerAction is None:
                gameState = GameState2048()
                continue
            gameState = gameState.generateSuccessor(1, computerAction)
        print "computer"
        print(gameState)
        lastState = gameState
        # print "board", gameState.board
        humanAction = move(gameState)
        gameState = gameState.generateSuccessor(0, humanAction)
        if gameState is None:
            gameState = GameState2048()
            continue
        print "human"
        print(gameState)