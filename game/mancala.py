import numpy as np


class Mancala:
    def __init__(self, holes=7, stones=7, board=None):
        self.n_holes = holes
        self.n_stones = stones
        self.north_store = self.n_holes
        self.south_store = self.n_holes * 2 + 1
        self.north = 'north'
        self.south = 'south'

        self.board = None
        self.reset(board)

    # make a board of initial state
    def reset(self, board=None):
        if board is None:
            # +1 for store, * 2 for two players
            self.board = np.full((self.n_holes + 1) * 2, self.n_stones)
            # set store stones to 0
            self.board[self.n_holes] = 0
            self.board[-1] = 0
        else:
            self.board = board

    # select a hole to move by player
    def step(self, side, hole):
        pos = self._get_board_pos(side, hole)
        stones = self.board[pos]
        self.board[pos] = 0
        pos += 1
        last_pos = pos
        # record the position where last stone is placed
        while stones > 0:
            if not self._is_opponent_store(side, pos):
                self.board[pos] += 1
                stones -= 1
                if stones == 0:
                    last_pos = pos
            # increment position
            # if position outside the board make it start from the beginning of the board by %
            pos = (pos + 1) % len(self.board)

        return last_pos

    # return the position of player's scoring well
    def _get_store(self, side):
        return self.south_store if side == self.south else self.north_store

    def _get_opponent_store(self, side):
        return self.south_store if side == self.north else self.north_store

    # swap the player after each normal round
    def _get_opponent_side(self, side):
        return self.north if side == self.south else self.south

    # verify whether it is player's hole
    def _is_hole(self, side, pos):
        return side == self.south and self.north_store < pos < self.south_store \
               or side == self.north and pos < self.south_store

    # get the according opponent hole position given the self hole position
    def _get_opponent_mirror_pos(self, self_pos):
        assert self._is_hole(self.south, self_pos) or self._is_hole(self.north, self_pos)
        return 2 * self.n_holes - self_pos

    # verify whether is player's scoring well
    def _is_store(self, side, pos):
        return side == self.south and pos == self.south_store \
               or side == self.north and pos == self.north_store

    # verify whether is opponent's scoring well
    def _is_opponent_store(self, side, pos):
        return side == self.south and pos == self.north_store \
               or side == self.north and pos == self.south_store

    # get the position to move in the board array
    # assuming the side chosen is reasonable
    def _get_board_pos(self, side, hole):
        return hole - 1 if side == self.north else hole + self.n_holes

    # swap the side for north according to pie rule
    # assuming the swap instruction is reasonable
    def _swap_side(self):
        self.board = np.roll(self.board, self.n_holes + 1)
        # board_copy = deepcopy(self.board)
        # for i in range(len(self.board)):
        #     board_copy[i] = self.board[(i+self.n_holes+1)%len(self.board)]
        # self.board = board_copy

    # check whether the player has won
    def _has_over_half_stones(self, side):
        return self.board[self._get_store(side)] > 49

    def _get_start_hole(self, side):
        return 0 if side == self.north else self.n_holes + 1

    # check whether the player has legal move
    def _all_holes_empty(self, side):
        start = self._get_start_hole(side)
        return np.any(self.board[start:start + self.n_holes])

    # print the board
    def __str__(self):
        formatter = {'int': lambda x: f'{x: >3d}'}
        return '{:2d}  {}\n    {}  {}'.format(
            self.board[self.north_store],
            np.array2string(self.board[0:self.north_store][::-1], formatter=formatter),
            np.array2string(self.board[self.north_store + 1:self.south_store], formatter=formatter),
            self.board[self.south_store]
        )
