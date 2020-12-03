import sys
sys.path.append('..')
from agent import Agent
sys.path.append('../alpha_beta_pruning')
import alpha_beta_pruning
from mancala import Mancala

class AlphaPruningAgent(Agent):
    def get_move(board, side):
        mancala = Mancala(7,7,board)
        move, _ = alpha_beta_pruning.alpha_beta_pruning(mancala, side)
        return move
