from copy import deepcopy
from game.mancala import Mancala


class ABPMancala(Mancala):

    def __init__(self, holes, stones, board):
        super().__init__(holes, stones, board)

    @classmethod
    def from_mancala(cls, mancala):
        instance = cls(mancala.n_holes, mancala.n_stones, mancala.board)
        instance.last_pos = deepcopy(mancala.last_pos)
        instance.next_player = deepcopy(mancala.next_player)
        instance.game_over = deepcopy(mancala.game_over)
        instance.winner = deepcopy(mancala.winner)
        instance.move_history = deepcopy(mancala.move_history)
        return instance

    def step(self, side, hole):
        mancala_copy = Mancala(holes=self.n_holes, stones=self.n_stones, board=deepcopy(self.board))

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

        return ABPMancala.from_mancala(mancala_copy)
