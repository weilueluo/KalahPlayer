# import sys
# sys.path.append('..')
# from agent import Agent
# sys.path.append('../alpha_beta_pruning')
# import alpha_beta_pruning
# from mancala import Mancala

from agents.agent import Agent
from alpha_beta_pruning.abpmancala import ABPMancala
from alpha_beta_pruning.alpha_beta_pruning import alpha_beta_pruning


class AlphaPruningAgent(Agent):
    def get_move(self, game, side):
        mancala = ABPMancala(game.n_holes, game.n_holes, game.board)
        move, _ = alpha_beta_pruning(mancala, side)
        return move
