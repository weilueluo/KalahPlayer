import numpy as np


class Mancala:
    def __init__(self, holes=7, stones=7, board=None):
        self.n_holes = holes
        self.n_stones = stones
        self.north_store = self.n_holes
        self.south_store = self.n_holes * 2 + 1
        self.north = 'north'
        self.south = 'south'

        self.last_pos = None
        self.next_player = None
        self.game_over = None
        self.winner = None

        self.move_history = []
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
        self.last_pos = None
        self.next_player = None
        self.game_over = None
        self.winner = None
        self.move_history = []

    def empty_hole_end_game(self, side):
        def sum_side(side):
            start = self.get_start_hole(side)
            store = self.north_store if side == self.north else self.south_store
            self.board[store] = self.board[start:start + self.n_holes].sum()
            self.board[start:start + self.n_holes] = 0

        sum_side(self.north)
        sum_side(self.south)

        if self.board[self.get_store(side)] > self.board[self.get_opponent_store(side)]:
            # win game
            self.winner = side

        elif self.board[self.get_store(side)] < self.board[self.get_opponent_store(side)]:
            # lose game
            self.winner = self.get_opponent_side(side)
        else:
            # tie
            self.winner = None

        self.game_over = True

    def evaluate(self, side):
        if self.has_over_half_stones(side):
            # win game
            self.winner = side
            self.game_over = True

        elif self.has_over_half_stones(self.get_opponent_side(side)):
            # lose game
            self.winner = self.get_opponent_side(side)
            self.game_over = True

        # extra move reward
        elif self.is_store(side, self.last_pos):
            self.winner = None
            self.next_player = side
            self.game_over = False

        # if the last position is in an self empty hole while the according opponent's hole
        # has stones in it, take the stones from both holes
        elif self.is_hole(side, self.last_pos) and self.board[self.last_pos] == 1 \
                and self.board[self.get_opponent_mirror_pos(self.last_pos)] != 0:
            store = self.get_store(side)
            opponent_mirror_pos = self.get_opponent_mirror_pos(self.last_pos)
            extra_score = self.board[self.last_pos] + self.board[opponent_mirror_pos]
            self.board[store] += extra_score
            self.board[self.last_pos] = 0
            self.board[opponent_mirror_pos] = 0

            self.next_player = self.get_opponent_side(side)
            self.game_over = False

        # normal move that does not do anything
        else:
            self.next_player = self.get_opponent_side(side)
            self.game_over = False

        # check if a side is empty
        if self.all_holes_empty(self.north) or self.all_holes_empty(self.south):
            self.empty_hole_end_game(side)

    # select a hole to move by player
    def step(self, side, hole):
        hole = int(hole)
        if hole not in self.get_valid_moves(side):
            self.game_over = True
            self.winner = self.get_opponent_side(side)
        pos = self.get_board_pos(side, hole)
        stones = self.board[pos]
        self.board[pos] = 0
        pos += 1
        last_pos = pos
        # record the position where last stone is placed
        while stones > 0:
            if not self.is_opponent_store(side, pos):
                self.board[pos] += 1
                stones -= 1
                if stones == 0:
                    last_pos = pos
            # increment position
            # if position outside the board make it start from the beginning of the board by %
            pos = (pos + 1) % len(self.board)
        self.last_pos = last_pos
        self.evaluate(side)
        self.move_history.append((side, hole, self.__str__()))

    # return the position of player's scoring well
    def get_store(self, side):
        return self.south_store if side == self.south else self.north_store

    def get_opponent_store(self, side):
        return self.south_store if side == self.north else self.north_store

    # swap the player after each normal round
    def get_opponent_side(self, side):
        return self.north if side == self.south else self.south

    # verify whether it is player's hole
    def is_hole(self, side, pos):
        return (side == self.south and self.north_store < pos < self.south_store) \
               or (side == self.north and 0 < pos < self.north_store)

    # get the according opponent hole position given the self hole position
    def get_opponent_mirror_pos(self, self_pos):
        assert self.is_hole(self.south, self_pos) or self.is_hole(self.north, self_pos)
        return 2 * self.n_holes - self_pos

    # verify whether is player's scoring well
    def is_store(self, side, pos):
        return side == self.south and pos == self.south_store \
               or side == self.north and pos == self.north_store

    # verify whether is opponent's scoring well
    def is_opponent_store(self, side, pos):
        return side == self.south and pos == self.north_store \
               or side == self.north and pos == self.south_store

    # get the position to move in the board array
    # assuming the side chosen is reasonable
    def get_board_pos(self, side, hole):
        return hole - 1 if side == self.north else hole + self.n_holes

    # swap the side for north according to pie rule
    # assuming the swap instruction is reasonable
    def swap_side(self):
        self.board = np.roll(self.board, self.n_holes + 1)

    # check whether the player has won
    def has_over_half_stones(self, side):
        return self.board[self.get_store(side)] > (self.n_holes * self.n_stones)

    def get_start_hole(self, side):
        return 0 if side == self.north else self.n_holes + 1

    # check whether the player has legal move
    def all_holes_empty(self, side):
        start = self.get_start_hole(side)
        return not np.any(self.board[start:start + self.n_holes])

    # find all valid move for a side
    def get_valid_moves(self, side):
        return np.nonzero(self.get_holes(side))[0] + 1

    def get_holes(self, side):
        start = self.get_start_hole(side)
        return self.board[start:start+self.n_holes]

    # print the board
    def __str__(self):
        formatter = {'int': lambda x: f'{x: >3d}'}
        return '{:2d}  {}\n    {}  {}'.format(
            self.board[self.north_store],
            np.array2string(self.board[0:self.north_store][::-1], formatter=formatter),
            np.array2string(self.board[self.north_store + 1:self.south_store], formatter=formatter),
            self.board[self.south_store]
        )