import numpy as np

from .mancala import Mancala


class MancalaEnv(Mancala):
    def __init__(self, holes=7, stones=7, board=None):
        super().__init__(holes, stones, board)
        self.history = []

    def reset(self, board=None):
        super().reset(board)
        self.history = []

    # def empty_hole_end_game(self, side):
    #     def sum_side(side):
    #         start = self.get_start_hole(side)
    #         store = self.north_store if side == self.north else self.south_store
    #         self.board[store] = self.board[start:start + self.n_holes].sum()
    #         self.board[start:start + self.n_holes] = 0
    #
    #     sum_side(self.north)
    #     sum_side(self.south)
    #
    #     if self.board[self.get_store(side)] > self.board[self.get_opponent_store(side)]:
    #         # win game
    #         score = reward_end_game
    #         winner = side
    #     elif self.board[self.get_store(side)] < self.board[self.get_opponent_store(side)]:
    #         # lose game
    #         score = -reward_end_game
    #         winner = self.get_opponent_side(side)
    #     else:
    #         # tie
    #         score = 0
    #         winner = None
    #     return winner, score, True

    # evaluate the current status of the game
    def _evaluate(self, side, move, score_increase):
        if self.game_over and self.winner == side:
            reward = 100
        elif self.game_over and self.winner == self.get_opponent_side(side):
            reward = -100
        elif self.game_over and self.winner is None:
            reward = -1
        else:
            reward = score_increase

        self.history.append((side, move, reward, self.__str__()))
        return self.next_player, reward, self.game_over

    # select a hole to move by player
    # returns: next_move_player, score_for_this_move, game_has_ended
    def step(self, side, hole):
        score_before = self.board[self.get_store(side)]
        super().step(side, hole)
        score_after = self.board[self.get_store(side)]

        if hole not in self.get_valid_moves(side):
            return self.next_player, -100, self.game_over

        return self._evaluate(side, hole, score_after - score_before)
