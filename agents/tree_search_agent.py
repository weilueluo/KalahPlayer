from agents.agent import Agent
import sys
sys.path.append('./tree_search')
from tree_search import MCTS

class MCTSAgent(Agent):

    def get_move(self, game, side):
        move = MCTS.UCT(rootGame=game, side=side)
        return move
