#!/usr/bin/env python3

from typing import List, Tuple
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
        self.board = [[None] * self.cols for _ in range(self.rows)]
        self.score = 0

    def get_open_squares(self) -> List:
        return [(row, col) for row in range(self.rows) for col in range(self.cols) if self.board[row][col] is None]

    def add_square(self) -> bool:
        open_squares = self.get_open_squares()
        if len(open_squares) == 0:
            return False
        else:
            square = random.choice(open_squares)
            self.board[square[0]][square[1]] = random.choice(self.NEW_VALUES)
            return True

    def collapse(self, values: Tuple) -> List:
        '''
        Collapses from left to right:
        [2, 2, 4, 1] -> [None, 4, 4, 1]
        [None, 4, 4, 4] -> [None, None, 4, 8]
        '''
        collapsed = list(values)
        i = len(collapsed) - 1
        while i > 0:
            if collapsed[i] is None:
                collapsed.pop(i)
            elif collapsed[i] == collapsed[i - 1]:
                collapsed[i] *= 2
                collapsed.pop(i - 1)
                i -= 1
            i -= 1
        return [None] * (len(values) - len(collapsed)) + collapsed

    def make_move(self, move: Move) -> None:
        if move == Move.left:
            pass
        elif move == Move.up:
            pass
        elif move == Move.right:
            pass
        elif move == Move.down:
            pass
        raise NotImplementedError()