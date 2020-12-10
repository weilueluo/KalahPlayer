# import sys
# sys.path.append('..')
# from agent import Agent
# sys.path.append('../alpha_beta_pruning')
# import alpha_beta_pruning
# from mancala import Mancala

from agents.agent import Agent
from alpha_beta_pruning.alpha_beta_pruning import alpha_beta_pruning
from game.mancala import Mancala


class AlphaPruningAgent(Agent):
    def __init__(self, max_depth=4, process_depth=0, thread_depth=0):
        self.max_depth = max_depth
        self.process_depth = process_depth
        self.thread_depth = thread_depth

    def get_move(self, game, side):
        mancala = Mancala(game.n_holes, game.n_holes, game.board)
        return alpha_beta_pruning(mancala, side,
                                  max_depth=self.max_depth,
                                  max_process_depth=self.process_depth,
                                  max_threading_depth=self.thread_depth)
