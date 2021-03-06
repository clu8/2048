﻿from typing import List, Tuple, Iterable
import random
from enum import Enum

class Move(Enum):
    left = 1
    up = 2
    right = 3
    down = 4

class Game(object):
    NEW_VALUES = [2, 4]

    def __init__(self, rows=4, cols=4) -> None:
        self.rows = rows
        self.cols = cols
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.score = 0

    def __str__(self) -> str:
        def serialize(value: int) -> str:
            s = '.' if value == 0 else str(value)
            return '{:4}'.format(s)

        return 'Score: {}\n'.format(self.score) + \
            '\n'.join([' '.join([serialize(self.board[r][c]) for c in range(self.cols)]) 
                       for r in range(self.rows)])

    def get_open_squares(self) -> List[Tuple[int, int]]:
        return [(row, col) for row in range(self.rows) for col in range(self.cols) if self.board[row][col] == 0]

    def add_square(self) -> bool:
        open_squares = self.get_open_squares()
        if len(open_squares) == 0:
            return False
        else:
            square = random.choice(open_squares)
            self.board[square[0]][square[1]] = random.choice(self.NEW_VALUES)
            return True

    def collapse(self, values: Iterable[int]) -> List[int]:
        '''
        Collapses from left to right:
        [2, 2, 4, 1] -> [0, 4, 4, 1]
        [0, 4, 4, 4] -> [0, 0, 4, 8]
        '''
        collapsed = list([x for x in values if x != 0])
        i = len(collapsed) - 1
        while i > 0:
            if collapsed[i] == collapsed[i - 1]:
                collapsed[i] *= 2
                collapsed.pop(i - 1)
                i -= 1
            i -= 1
        return [0] * (len(values) - len(collapsed)) + collapsed

    def make_move(self, move: Move) -> None:
        if move == Move.right:
            self.board = [self.collapse(row) for row in self.board]
        elif move == Move.left:
            self.board = [self.collapse(row[::-1])[::-1] for row in self.board]
        elif move == Move.down:
            transposed = list(zip(*self.board))
            collapsed = [self.collapse(col) for col in transposed]
            self.board = list([list(x) for x in zip(*collapsed)])
        elif move == Move.up:
            transposed = list(zip(*self.board))
            collapsed = [self.collapse(col[::-1])[::-1] for col in transposed]
            self.board = list([list(x) for x in zip(*collapsed)])
