from copy import deepcopy
from game.mancala import Mancala


class ABPMancala(Mancala):

    def step(self, side, hole):
        mancala_copy = deepcopy(self)

        mancala_copy.step(side, hole)

        last_pos = mancala_copy.last_pos

        if mancala_copy.is_self_store(side, last_pos):
            return mancala_copy

        if mancala_copy.is_self_hole(side, last_pos) and mancala_copy.board[last_pos] == 1 \
                and mancala_copy.board[mancala_copy.get_opponent_pos(last_pos)] != 0:
            scores_stored = mancala_copy.get_self_store(side)
            mancala_copy.board[scores_stored] = mancala_copy.board[scores_stored] + mancala_copy.board[last_pos] \
                                           + mancala_copy.board[mancala_copy.get_opponent_pos(last_pos)]
            mancala_copy.board[last_pos] = 0
            mancala_copy.board[mancala_copy.get_opponent_pos(last_pos)] = 0

        return mancala_copy
