import numpy as np

from .mancala import Mancala

reward_end_game = 100


class MancalaEnv(Mancala):
    def __init__(self, holes=7, stones=7, board=None):
        super().__init__(holes, stones, board)
        self.move_history = []

    def reset(self, board=None):
        super().reset(board)
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
            score = reward_end_game
            winner = side
        elif self.board[self.get_store(side)] < self.board[self.get_opponent_store(side)]:
            # lose game
            score = -reward_end_game
            winner = self.get_opponent_side(side)
        else:
            # tie
            score = 0
            winner = None
        return winner, score, True

    # evaluate the current status of the game
    def _evaluate(self, side, last_pos, move, score_increase):

        if self.has_over_half_stones(side):
            # win game
            next_move_player = side
            score = reward_end_game
            game_ended = True
            self.winner = side
        elif self.has_over_half_stones(self.get_opponent_side(side)):
            # lose game
            next_move_player = self.get_opponent_side(side)
            score = -reward_end_game
            game_ended = True
            self.winner = self.get_opponent_side(side)

        # extra move reward
        elif self.is_store(side, last_pos):
            next_move_player = side
            score = 3
            game_ended = False

        # if the last position is in an self empty hole while the according opponent's hole
        # has stones in it, take the stones from both holes
        elif self.is_hole(side, last_pos) and self.board[last_pos] == 1 \
                and self.board[self.get_opponent_mirror_pos(last_pos)] != 0:
            store = self.get_store(side)
            opponent_mirror_pos = self.get_opponent_mirror_pos(last_pos)
            extra_score = self.board[last_pos] + self.board[opponent_mirror_pos]
            self.board[store] += extra_score
            self.board[last_pos] = 0
            self.board[opponent_mirror_pos] = 0

            next_move_player = self.get_opponent_side(side)
            score = 0
            game_ended = False

        # normal move that does noy do anything
        else:
            next_move_player = self.get_opponent_side(side)
            score = 0
            game_ended = False

        # check if a side is empty
        if self.all_holes_empty(self.north) or self.all_holes_empty(self.south):
            next_move_player, score, game_ended = self.empty_hole_end_game(side)

        elif not game_ended:
            score += score_increase

        self.move_history.append((side, move, score, self.__str__()))
        return next_move_player, score, game_ended

    # select a hole to move by player
    # returns: next_move_player, score_for_this_move, game_has_ended
    def step(self, side, hole):
        hole = int(hole)
        if hole not in self.get_valid_moves(side):
            return None, -reward_end_game, True
        score_before = self.board[self.get_store(side)]
        last_pos = super().step(side, hole)
        score_after = self.board[self.get_store(side)]
        return self._evaluate(side, last_pos, hole, score_after - score_before)
