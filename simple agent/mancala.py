import numpy as np

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

    # make a board of initial state
    def reset(self):
        self.board = np.full((self.n_holes + 1) * 2, self.n_stones)
        self.board[self.n_holes] = 0
        self.board[-1] = 0
        self.first_play = True

    def _post_step(self, side, last_pos):
        # if last position is in the player's scoring well and is not first play
        # instruct an extra move
        if self.is_store(side, last_pos) and not self.first_play:
            return f'{side}:continue'

        # if the last position is in an self empty hole while the according opponent's hole
        # has stones in it, take the stones from both holes
        if self.is_hole(side, last_pos) and self.board[last_pos] == 1 \
            and self.board[self.get_opponent_pos(last_pos)] != 0:
            scores_stored_pos = self.get_store(side)
            self.board[scores_stored_pos] = self.board[scores_stored_pos]+ self.board[last_pos] \
                + self.board[self.get_opponent_pos(last_pos)]
            self.board[last_pos] = 0
            self.board[self.get_opponent_pos(last_pos)] = 0


        # record first play
        if self.first_play:
            self.first_play = False

        # if the player has won, print out the message
        if self.has_over_half_stones(side):
            return f'{side}:has won'
        else:
            return self.get_opponent_side(side)

    # select a hole to move by player
    def step(self, side, hole):
        if not self.has_legal_move(side):
            return self.check_win()

        pos = self._get_board_pos(side, hole)
        stones = self.board[pos]
        self.board[pos] = 0
        pos += 1
        # record the position where last stone is placed
        last_pos = pos
        while stones > 0:
            if not self.is_opponent_store(side, pos):
                self.board[pos] += 1
                stones -= 1
                if stones == 0:
                    last_pos = pos
            # add the position
            # if position outside the board make it start from the beginning of the board by %
            pos = (pos + 1) % len(self.board)

        return self._post_step(side, last_pos)


    # return the position of player's scoring well
    def get_store(self, side):
        return self.south_store if side == self.south else self.north_store

    # swap the player after each normal round
    def get_opponent_side(self, side):
        return self.north if side == self.south else self.south

    # verify whether it is player's hole
    def is_hole(self, side, pos):
        return side == self.south and self.north_store < pos < self.south_store \
            or side == self.north and pos < self.south_store

    # get the according opponent hole position given the self hole position
    def get_opponent_pos(self, self_pos):
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
    def _get_board_pos(self, side, hole):
        return hole - 1 if side == self.north else hole + self.n_holes

    # swap the side for north according to pie rule
    # assuming the swap instruction is reasonable
    def swap_side(self):
        self.board = np.roll(self.board, self.n_holes + 1)
        return "swapped:south"
        # board_copy = deepcopy(self.board)
        # for i in range(len(self.board)):
        #     board_copy[i] = self.board[(i+self.n_holes+1)%len(self.board)]
        # self.board = board_copy

    # check whether the player has won
    def has_over_half_stones(self, side):
        return self.board[self.get_store(side)] > 49

    def get_start_hole(self, side):
        return 0 if side == self.north else self.n_holes + 1

    # check whether the player has legal move
    def has_legal_move(self, side):
        start = self.get_start_hole(side)
        return np.any(self.board[start:start + self.n_holes])
        # for i in range (self.n_holes):
        #     if self.board[i+offset] > 0:
        #         return True
        # return False

    # when one player does not have legal move
    # check the board to see who has won
    def check_win(self):
        north_total = self.board[self.get_store(self.north)]
        south_total = self.board[self.get_store(self.south)]
        offset = self.n_holes+1
        for i in range (self.n_holes):
            north_total += self.board[i]
            self.board[i] = 0
        self.board[self.get_store(self.north)] = north_total
        for i in range (self.n_holes):
            south_total += self.board[i+offset]
            self.board[i+offset] = 0
        self.board[self.get_store(self.south)] = south_total
        if north_total == south_total:
            return "draw"
        elif north_total > south_total:
            return "north:has won"
        else:
            return "south:has won"

    # print out of the board
    def __str__(self):
        formatter = {'int': lambda x: f'{x: >3d}'}
        return '{:2d}  {}\n    {}  {}'.format(
            self.board[self.north_store],
            np.array2string(self.board[0:self.north_store][::-1], formatter=formatter),
            np.array2string(self.board[self.north_store+1:self.south_store], formatter=formatter),
            self.board[self.south_store]
        )
