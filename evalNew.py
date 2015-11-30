def eval_numempty(board):
    '''
    Number of empty squares in board. 
    '''
    return sum([row.count(0) for row in board])

def eval_smoothness(board):
    '''
    Sum the difference between each pair of adjacent tiles. Smaller is better so we take its reciprocal. 
    '''
    def row_smoothness(board):
        return sum([abs(r[c] - r[c+1]) for r in board for c in range(len(r) - 1)])

    return 1 / (row_smoothness(board) + row_smoothness(zip(*board)) + 1)

def eval_monotonicity(board):
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

    return 1 / (row_monotonicity(board) + row_monotonicity(zip(*board)) + 1)

def eval_combined(board, empty_weight=1.0, smoothness_weight=10.0, 
                  monotonicity_weight=5.0):
    return empty_weight * eval_numempty(board) + smoothness_weight * eval_smoothness(board) \
        + monotonicity_weight * eval_monotonicity(board)