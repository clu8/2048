import util

def eval_numempty(state):
    '''
    Number of empty squares in board. 
    '''
    return sum([row.count(0) for row in state.board])

def eval_smoothness(state):
    '''
    Sum the difference between each pair of adjacent tiles. Smaller is better so we take its reciprocal. 
    '''
    def row_smoothness(board):
        return sum([abs(r[c] - r[c+1]) for r in board for c in range(len(r) - 1)])

    return 1 / (row_smoothness(state.board) + row_smoothness(zip(*state.board)) + 1)

def eval_monotonicity(state):
    '''
    Eval function which measures how much the rows and cols are sorted in increasing or descending order. 
    Specifically we count the total number of times the rows and cols switch from increasing to decreasing or vice versa. 
    Smaller is better so we take its reciprocal. 
    '''
    def row_monotonicity(board):
        switches = 0
        for r in board:
            increasing = None
            for c in range(len(r) - 1):
                if r[c+1] > r[c]:
                    if increasing == False:
                        switches += 1
                    increasing = True
                elif r[c+1] < r[c]:
                    if increasing == True:
                        switches += 1
                    increasing = False
        return switches

    return 1.0 / (row_monotonicity(state.board) + row_monotonicity(zip(*state.board)) + 1)

def eval_combined(state, empty_weight=1.0, smoothness_weight=10.0, 
                  monotonicity_weight=5.0):
    return empty_weight * eval_numempty(state) + smoothness_weight * eval_smoothness(state) \
        + monotonicity_weight * eval_monotonicity(state)

SNAKE_WEIGHTS = [4 ** 15, 4 ** 14, 4 ** 13, 4 ** 12,
                 4 ** 8, 4 ** 9, 4 ** 10, 4 ** 11,
                 4 ** 7, 4 ** 6, 4 ** 5, 4 ** 4,
                 4 ** 0, 4 ** 1, 4 ** 2, 4 ** 3]
def eval_snake(state):
    '''
    Linear combination of all squares' values. 
    Inspired by Hadi Pouransari & Saman Ghili's "AI algorithms for the game 2048".
    '''
    return util.dot_product(SNAKE_WEIGHTS, util.unroll_board(state.board))

def eval_snake_and_empty(state):
    return eval_snake(state.board) + 2 ** eval_numempty(state.board)