from typing import List

def eval_numempty(board: List[List[int]]):
    '''
    Number of empty squares in board. 
    '''
    return sum([row.count(0) for row in board])

def eval_smoothness(board: List[List[int]]):
    '''
    Sum the difference between each pair of adjacent tiles. Smaller is better so we take its reciprocal. 
    '''
    smoothness = 0
    for r in board:
        for c in range(len(r) - 1):
            smoothness += abs(r[c] - r[c+1])

    transposed = zip(*board)
    for c in transposed:
        for r in range(len(c) - 1):
            smoothness += abs(c[r] - c[r+1])

    return 1 / (smoothness + 1)

def eval_monotonicity():
    pass