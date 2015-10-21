﻿# use pytest
from Game import *

class TestGame:
    def test_board_creation(self):
        g = Game()
        assert len(g.get_open_squares()) == 4 * 4
        assert len(g.board) == 4
        assert len(g.board[0]) == 4

        g2 = Game(5, 6)
        assert len(g2.get_open_squares()) == 5 * 6
        assert len(g2.board) == 5
        assert len(g2.board[0]) == 6

    def test_open_squares(self):
        g = Game()
        open_squares = g.get_open_squares()
        for row in range(4):
            for col in range(4):
                assert (row, col) in open_squares

    def test_add_square(self):
        g = Game()
        for i in range(16):
            print(len(g.get_open_squares()))
            assert g.add_square() == True
            print(len(g.get_open_squares()))
            assert len(g.get_open_squares()) == 15 - i
        assert g.add_square() == False
        assert len(g.get_open_squares()) == 0

    def test_collapse(self):
        g = Game()
        assert g.collapse((2, 2, 4, 1)) == [None, 4, 4, 1]
        assert g.collapse((None, 4, 4, 4)) == [None, None, 4, 8]
        assert g.collapse((4, 8, 32, 4)) == [4, 8, 32, 4]
        assert g.collapse((2, None, None, None)) == [None, None, None, 2]
        assert g.collapse((None, None, None, 2)) == [None, None, None, 2]
        assert g.collapse((2, 2, 4, 4)) == [None, None, 4, 8]
        assert g.collapse((2, 2, 4, 8)) == [None, 4, 4, 8]
        assert g.collapse((8, 8, None, None)) == [None, None, None, 16]