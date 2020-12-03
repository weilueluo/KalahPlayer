import random
# import numpy as np
# from copy import deepcopy
# from mancala import Mancala
# import sys
# sys.path.append('..')
# from agent import Agent

from agents.agent import Agent


class RandomAgent(Agent):


    # def get_move(self, env, side):
    #     game = Mancala(n_holes, n_holes, board=deepcopy(env.board))
    #     return np.random.choice(game.get_valid_moves(side), 1, replace=False)[0]

    # return a move
    def get_move(self, game, side):
        board = game.board
        if side == 'north':
            offset = 1
        else:
            offset = -7
        # find available moves
        available_moves = RandomAgent.get_available_move(board, side)
        # get a random move
        move = RandomAgent.get_random_move(available_moves)
        # convert the move from board index to move
        move += offset
        print("Random move is: " + str(move))
        return move

    # get the valid moves in the board
    # return the array of available move positions(in index) in board
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

    # get a random move from the available moves
    @staticmethod
    def get_random_move(available_moves):
        return random.choice(available_moves)
