import numpy as np

from .mancala import Mancala


class MancalaEnv(Mancala):
    def __init__(self, holes=7, stones=7, board=None):
        super().__init__(holes, stones, board)
        self.move_history = None

    def reset(self, board=None):
        super().reset(board)
        self.move_history = []

    # evaluate the current status of the game
    def _evaluate(self, side, last_pos, move, store_score_diff):

        if self._has_over_half_stones(side):
            # win game
            next_move_player = None
            score = 100
            game_ended = True
        elif self._has_over_half_stones(self._get_opponent_side(side)):
            # lose game
            next_move_player = None
            score = -100
            game_ended = True

        # if any side's hole is empty
        elif self._all_holes_empty(self.north) or self._all_holes_empty(self.south):
            def sum_side(side):
                start = self._get_start_hole(side)
                store = self.north_store if side == self.north else self.south_store
                self.board[store] = self.board[start:start + self.n_holes].sum()
                self.board[start:start + self.n_holes] = 0

            sum_side(self.north)
            sum_side(self.south)

            if self.board[self._get_store(side)] > self.board[self._get_opponent_store(side)]:
                # win game
                next_move_player = None
                score = 100
                game_ended = True
            elif self.board[self._get_store(side)] < self.board[self._get_opponent_store(side)]:
                # lose game
                next_move_player = None
                score = -100
                game_ended = True
            else:
                # tie
                next_move_player = None
                score = 0
                game_ended = True

        # extra move reward
        elif self._is_store(side, last_pos):
            next_move_player = side
            score = 5
            game_ended = False

        # if the last position is in an self empty hole while the according opponent's hole
        # has stones in it, take the stones from both holes
        elif self._is_hole(side, last_pos) and self.board[last_pos] == 1 \
                and self.board[self._get_opponent_mirror_pos(last_pos)] != 0:
            store = self._get_store(side)
            opponent_mirror_pos = self._get_opponent_mirror_pos(last_pos)
            extra_score = self.board[last_pos] + self.board[opponent_mirror_pos]
            self.board[store] += extra_score
            self.board[last_pos] = 0
            self.board[opponent_mirror_pos] = 0

            next_move_player = self._get_opponent_store(side)
            score = extra_score
            game_ended = False

        # normal move that add more stones to own store
        elif store_score_diff > 0:
            next_move_player = self._get_opponent_side(side)
            score = self.board[self._get_store(side)] - store_score_diff
            game_ended = False

        # normal move that does not change different between scored stones
        else:
            next_move_player = self._get_opponent_side(side)
            score = 0
            game_ended = False

        self.move_history.append((side, move, score))
        return next_move_player, score, game_ended

    # select a hole to move by player
    # returns: next_move_player, score_for_this_move, game_has_ended
    def step(self, side, hole):
        # print("In step, side:", side, "hole:", hole)
        if hole not in self.get_valid_moves(side):
            return None, -100, True

        my_score_before_move = self.board[self._get_store(side)]
        opponent_score_before_move = self.board[self._get_opponent_store(side)]

        last_pos = super().step(side, hole)

        my_score_after_move = self.board[self._get_store(side)]
        opponent_score_after_move = self.board[self._get_opponent_store(side)]

        store_score_diff = (my_score_after_move - my_score_before_move) \
                           - (opponent_score_after_move - opponent_score_before_move)

        return self._evaluate(side, last_pos, hole, store_score_diff)
