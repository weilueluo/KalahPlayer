
#Used as input for alpha_beta_pruning
import numpy as np
from copy import deepcopy
class Mancala:
    def __init__(self, holes=7, stones=7, board=None):
        self.n_holes = holes
        self.n_stones = stones
        self.north_store = self.n_holes
        self.south_store = self.n_holes * 2 + 1
        self.north = 'north'
        self.south = 'south'
        self.first_play = None
        self.reset()

        if board is not None:
            self.board = board


    def reset(self):
        self.board = np.full((self.n_holes+1) * 2, self.n_stones)
        self.board[self.n_holes] = 0
        self.board[-1] = 0
    @staticmethod
    def step(mancala, side, hole):
        mancala = deepcopy(mancala)
        pos = mancala.get_board_pos(side, hole)
        stones = mancala.board[pos]
        mancala.board[pos] = 0
        pos += 1
        last_pos = 0
        while stones > 0:
            if not mancala.is_opponent_store(side, pos):
                mancala.board[pos] += 1
                stones -= 1
                if stones == 0:
                    last_pos = pos
            pos = (pos + 1) % len(mancala.board)
        if mancala.is_self_store(side, last_pos):
            return mancala

        if mancala.is_self_hole(side, last_pos) and mancala.board[last_pos] == 1 \
            and mancala.board[mancala.get_opponent_pos(last_pos)] != 0:
            scores_stored = mancala.get_self_store(side)
            mancala.board[scores_stored] = mancala.board[scores_stored]+ mancala.board[last_pos] \
                + mancala.board[mancala.get_opponent_pos(last_pos)]
            mancala.board[last_pos] = 0
            mancala.board[mancala.get_opponent_pos(last_pos)] = 0

        return mancala

    def get_store(self, side):
        return self.south_store if side == self.south else self.north_store


    def get_self_store(self,side):
        if side == 'south':
            return self.south_store
        else:
            return self.north_store
    def get_opponent_side(self, side):
        if side == 'north':
            return 'south'
        else:
            return 'north'

    def is_self_hole(self, side, pos):
        return side == 'south' and self.north_store < pos < self.south_store \
            or side == 'north' and -1 < pos < self.north_store

    def get_opponent_pos(self, pos):
        return 2 * self.n_holes - pos

    def is_self_store(self,side, pos):
        return side == 'south' and pos == self.south_store \
            or side == 'north' and pos == self.north_store


    def is_opponent_store(self, side, pos):
        return side == 'south' and pos == self.north_store \
            or side == 'north' and pos == self.south_store

    def get_board_pos(self, side, hole):
        return hole - 1 if side == 'north' else hole + self.n_holes

    def has_over_half_stones(self, side):
        return self.board[self.get_store(side)] > 49

    def __str__(self):
        formatter = {'int': lambda x: f'{x: >3d}'}
        return '{:2d}  {}\n    {}  {}'.format(
            self.board[self.north_store],
            np.array2string(self.board[0:self.north_store][::-1], formatter=formatter),
            np.array2string(self.board[self.north_store+1:self.south_store], formatter=formatter),
            self.board[self.south_store]
        )
