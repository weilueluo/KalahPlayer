import random
import numpy as np
from copy import deepcopy
from game.mancala import Mancala
import sys

sys.path.append('..')
from agents.agent import Agent


class SimpleAgent(Agent):
    # return a move
    def get_move(self, game, side):
        board = game.board
        if side == 'north':
            offset = 1
        else:
            offset = -7
        # find available moves
        available_moves = SimpleAgent.get_available_move(board, side)
        # get the suggested move
        move = SimpleAgent.get_suggested_move(board, side, available_moves)
        # convert the move from board index to move
        move += offset
        print("Suggest move is: " + str(move))
        return move

    # get the valid moves in the board
    # return the array of available move positions(in index) in board
    @staticmethod
    def get_available_move(board, side):
        valid_moves = []
        if side == 'north':
            offset = 0
        else:
            offset = 8
        # as long as the hole is empty, it is an available move
        for i in range(7):
            if (board[i + offset] != 0):
                valid_moves.append(i + offset)
        return valid_moves

    # check the increase in scores after a move
    @staticmethod
    def points_increase(old_board, new_board, side):
        if side == 'north':
            scoring_pos = 7
        else:
            scoring_pos = 15
        return new_board[scoring_pos] - old_board[scoring_pos]

    # check the max the player can got in the coming move
    # do not take into account extra moving case
    # in the SimpleAgent, it calculates the opponent's max increase
    @staticmethod
    def max_increase_normal(board, side, available_moves):
        # list to store all the increase in scores for each
        # avaliable moves
        scores_increase = []
        game = Mancala()
        # do a move to avoid pie rule
        game.step('north', 1)
        if side == 'north':
            offset = 1
        else:
            offset = -7
        # perform moves for available moves
        for i in available_moves:
            newboard = deepcopy(board)
            game.board = newboard
            game.step(side, i + offset)
            scores_increase.append(SimpleAgent.points_increase(board, game.board, side))
        return max(scores_increase)

    # suggests a move using simple rules
    @staticmethod
    def get_suggested_move(board, side, available_moves):
        game = Mancala()
        # do a move to avoid pie rule
        game.step('north', 1)
        if side == 'north':
            offset = 1
            oppo = 'south'
        else:
            offset = -7
            oppo = 'north'
        # if there is only one available move,
        # simply return that move
        if len(available_moves) == 1:
            return available_moves[0]
        # create a list to record the position_score of each position
        # it takes into account maximise self points
        # minimize opponent points and the availability of self extra move
        position_scores = []
        # i is the index of the position available
        for i in available_moves:
            newboard = deepcopy(board)
            game.board = newboard
            # info = game.step(side, i + offset)
            game.step(side, i + offset)
            # if the move can lead to win, perform that move
            # if info == (side + ':has won'):
            if game.winner == side:
                # print("detected a wining move......")
                return i
            # else, record the position score
            position_score = 0
            # if it can give an extra move, it get the point depend on how
            # close it is to the self scoring well
            # if info == (side + ':continue'):
            if game.next_player == side:
                # print("has an extra move")
                position_score += (i + offset)
            # it can also get the score according to how much points it can bring
            position_score += SimpleAgent.points_increase(board, game.board, side)
            # it will get an negative score when its opponent can increase their point
            oppo_available = SimpleAgent.get_available_move(game.board, oppo)
            position_score -= SimpleAgent.max_increase_normal(board, oppo, oppo_available)
            position_scores.append(position_score)
        # print("The position scores")
        # print(position_scores)
        return available_moves[position_scores.index(max(position_scores))]
