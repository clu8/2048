#!/usr/bin/env python3

from typing import List
import random

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