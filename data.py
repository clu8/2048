'''
Module for reading and writing move data to train reflex agents.
We store data in CSV files with 17 columns - 16 for the board state and 1 for the label (best move).
'''

import util
import csv

DATA_FILE_PATH = 'data/expectimax_depth3_moves.csv'

class MoveWriter(object):
    def __enter__(self, file_path=DATA_FILE_PATH):
        self.f = open(file_path, 'a')
        self.writer = csv.writer(self.f)
        return self

    def __exit__(self, type, value, traceback):
        self.f.__exit__(type, value, traceback)

    def write_move(self, board, move):
        self.writer.writerow(util.unroll_board(board) + (move,))

def read_data(file_path=DATA_FILE_PATH):
    '''
    Reads data CSV file and returns a list of ((unrolled board), move) data points.
    '''
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = [(tuple(row[:-1]), row[-1]) for row in reader]
    return data