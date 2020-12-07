import numpy as np

from .mancala import Mancala


class MancalaEnv(Mancala):
    def __init__(self, holes=7, stones=7, board=None):
        super().__init__(holes, stones, board)
        self.history = []

    def reset(self, board=None):
        super().reset(board)
        self.history = []

    # evaluate the current status of the game
    def _evaluate(self, side, move, score_increase):
        if self.game_over and self.winner == side:
            reward = 100
        elif self.game_over and self.winner == self.get_opponent_side(side):
            reward = -100
        elif self.game_over and self.winner is None:
            reward = -1  # encourage win instead of draw
        else:
            reward = score_increase

        self.history.append((side, move, reward, self.__str__()))
        return self.next_player, reward, self.game_over

    # select a hole to move by player
    # returns: next_move_player, score_for_this_move, game_has_ended
    def step(self, side, hole):
        score_before = self.board[self.get_store(side)]
        opp_score_before = self.board[self.get_opponent_store(side)]
        super().step(side, hole)
        score_after = self.board[self.get_store(side)]
        opp_score_after = self.board[self.get_opponent_store(side)]

        score_increase = (score_after - score_before) - (opp_score_after - opp_score_before)

        return self._evaluate(side, hole, score_increase)
