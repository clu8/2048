import pytest
from Game import *
from eval import *

class TestGame:
    board_1 = [[2, 0, 2, 2], 
               [0, 4, 0, 0], 
               [0, 0, 2, 0], 
               [4, 8, 0, 8]]

    board_2 = [[2, 2, 2],
               [4, 2, 0]]

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
            print((len(g.get_open_squares())))
            assert g.add_square() == True
            print((len(g.get_open_squares())))
            assert len(g.get_open_squares()) == 15 - i
        assert g.add_square() == False
        assert len(g.get_open_squares()) == 0

    def test_collapse(self):
        g = Game()
        assert g.collapse((2, 2, 4, 1)) == [0, 4, 4, 1]
        assert g.collapse((0, 4, 4, 4)) == [0, 0, 4, 8]
        assert g.collapse((4, 8, 32, 4)) == [4, 8, 32, 4]
        assert g.collapse((2, 0, 0, 0)) == [0, 0, 0, 2]
        assert g.collapse((0, 0, 0, 2)) == [0, 0, 0, 2]
        assert g.collapse((2, 2, 4, 4)) == [0, 0, 4, 8]
        assert g.collapse((2, 2, 4, 8)) == [0, 4, 4, 8]
        assert g.collapse((8, 8, 0, 0)) == [0, 0, 0, 16]
        assert g.collapse((4, 0, 4, 0)) == [0, 0, 0, 8]
        assert g.collapse((0, 4, 0, 4)) == [0, 0, 0, 8]

    def test_str(self):
        g = Game()
        g.board = self.board_1
        assert g.__str__() == 'Score: 0\n2    .    2    2   \n.    4    .    .   \n.    .    2    .   \n4    8    .    8   '

    @pytest.mark.parametrize('start,move,expected', [
        (board_1, Move.right, [[0, 0, 2, 4], 
                               [0, 0, 0, 4], 
                               [0, 0, 0, 2], 
                               [0, 0, 4, 16]]),
        (board_1, Move.left, [[4, 2, 0, 0],
                               [4, 0, 0, 0],
                               [2, 0, 0, 0],
                               [4, 16, 0, 0]]),
        (board_1, Move.down, [[0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [2, 4, 0, 2],
                               [4, 8, 4, 8]]),
        (board_1, Move.up, [[2, 4, 4, 2],
                               [4, 8, 0, 8],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]]),
        (board_2, Move.right, [[0, 2, 4],
                               [0, 4, 2]]),
        (board_2, Move.left, [[4, 2, 0],
                              [4, 2, 0]]),
        (board_2, Move.down, [[2, 0, 0],
                              [4, 4, 2]]),
        (board_2, Move.up, [[2, 4, 2],
                            [4, 0, 0]])
    ])
    def test_move(self, start, move, expected):
        g = Game()
        g.board = start

        g.make_move(move)
        result = g.board
        assert result == expected

        g.make_move(move)
        assert result == g.board

class TestEval:
    def test_eval_numempty(self):
        assert eval_numempty([[2, 2, 3, 0], [3, 0, 0, 4]]) == 3
        assert eval_numempty([[0 for c in range(4)] for r in range(4)]) == 16

    def test_eval_smoothness(self):
        assert eval_smoothness([[2, 0, 0, 2], [3, 4, 2, 3]]) == 1 / (16 + 1)
        assert eval_smoothness([[0 for c in range(4)] for r in range(4)]) == 1