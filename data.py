'''
Module for reading and writing move data to train reflex agents.
We store data in CSV files with 17 columns - 16 for the board state and 1 for the label (best move).
'''

import util
import csv

INPUTS_FILE_PATH = 'data/expectimax_depth2_inputs.csv'
LABELS_FILE_PATH = 'data/expectimax_depth2_labels.csv'

class MoveWriter(object):
    def __enter__(self, inputs_path=INPUTS_FILE_PATH, labels_path=LABELS_FILE_PATH):
        self.inputs_file = open(inputs_path, 'a')
        self.labels_file = open(labels_path, 'a')
        self.inputs_writer = csv.writer(self.inputs_file)
        self.labels_writer = csv.writer(self.labels_file)
        return self

    def __exit__(self, type, value, traceback):
        self.inputs_file.__exit__(type, value, traceback)
        self.labels_file.__exit__(type, value, traceback)

    def write_move(self, board, move):
        self.inputs_writer.writerow(util.unroll_board(board))
        self.labels_writer.writerow((move,))

def read_data(inputs_path=INPUTS_FILE_PATH, labels_path=LABELS_FILE_PATH):
    '''
    Reads data CSV file and returns a list of unrolled board inputs and a list of corresponding move labels.
    '''
    with open(inputs_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        inputs = [tuple(map(int, row)) for row in reader]

    with open(labels_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        labels = [tuple(map(int, row)) for row in reader]

    return (inputs, labels)

def fix():
    '''
    Small helper script to separate combined data CSV into inputs and labels CSV files. 
    '''
    with open(DATA_FILE_PATH, 'r') as original, open(INPUTS_FILE_PATH, 'w') as inputs, open(LABELS_FILE_PATH, 'w') as labels:
        reader = csv.reader(original)
        inputs_writer = csv.writer(inputs)
        labels_writer = csv.writer(labels)

        for row in reader:
            inputs_writer.writerow(row[:16])
            labels_writer.writerow(row[16:])