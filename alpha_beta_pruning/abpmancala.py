from copy import deepcopy
from game.mancala import Mancala


class ABPMancala(Mancala):

    def __init__(self, holes, stones, board):
        super().__init__(holes, stones, board)

    def step(self, side, hole):
        mancala_copy = Mancala(holes=self.n_holes, stones=self.n_stones, board=self.board)

        mancala_copy.step(side, hole)

        last_pos = mancala_copy.last_pos

        if mancala_copy.is_store(side, last_pos):
            return mancala_copy

        if mancala_copy.is_hole(side, last_pos) and mancala_copy.board[last_pos] == 1 \
                and mancala_copy.board[mancala_copy.get_opponent_mirror_pos(last_pos)] != 0:
            scores_stored = mancala_copy.get_store(side)
            mancala_copy.board[scores_stored] = mancala_copy.board[scores_stored] + mancala_copy.board[last_pos] \
                                           + mancala_copy.board[mancala_copy.get_opponent_mirror_pos(last_pos)]
            mancala_copy.board[last_pos] = 0
            mancala_copy.board[mancala_copy.get_opponent_mirror_pos(last_pos)] = 0

        return ABPMancala(holes=self.n_holes, stones=self.n_stones, board=mancala_copy.board)
