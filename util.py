import itertools

def unroll_board(board):
    '''
    Unrolls the board as a 2d list into a 1d tuple of 16 ints.
    '''
    return tuple(itertools.chain.from_iterable(board))

def dot_product(x, y):
    assert len(x) == len(y)
    return sum([a * b for (a, b) in zip(x, y)])