import torch
from copy import deepcopy
import numpy as np
from torch.functional import F
from models.mancala import MancalaModel
from agents.agent import Agent


class ModelAgent(Agent):
    def __init__(self, hidden_size=512, model_path=None, n_inputs=14, n_outputs=7, model=None, device='cpu',
                 model_cls=MancalaModel, neuron_size=512):
        assert model_path is not None or model is not None
        if model is not None:
            self.model = model
        else:
            self.model = model_cls(n_inputs, n_outputs, hidden_size=hidden_size, neuron_size=neuron_size)
            self.model.load_state_dict(torch.load(model_path))
            self.model.eval()
        self.hidden_size = hidden_size
        self.device = device
        self.hidden = None

    def init_hidden(self):
        self.hidden = (torch.zeros((1, self.hidden_size), dtype=torch.float, device=self.device),
                       torch.zeros((1, self.hidden_size), dtype=torch.float, device=self.device))

    def get_move(self, env, side):
        if not env.move_history:
            self.init_hidden()
        self.model.eval().to(self.device)
        with torch.no_grad():
            from models.train import get_model_input
            board = get_model_input(env, side).to(self.device)
            distribution, reward, self.hidden = self.model(board, self.hidden)
            action = np.argmax(distribution.cpu()).item() + 1
            return action

    # @staticmethod
    # def _as_one_hot(num, max):
    #     num = max if num > max else num
    #     one_hot = np.zeros((max,))
    #     one_hot[num-1] = 1
    #     return one_hot

#
# class ModelAgentV2:
#     def __init__(self, n_outputs, model_path=None, n_inputs=17, model=None):
#         self.n_outputs = n_outputs
#         if model is not None:
#             self.model = model
#         else:
#             self.model = MancalaModelV2(n_inputs)
#             self.model.load_state_dict(torch.load(model_path))
#
#     def get_move(self, env, side):
#         rewards = []
#         self.model.eval()
#         with torch.no_grad():
#             for move in range(1, self.n_outputs + 1):
#                 board = self.get_model_input(env.board, side, move)
#                 reward = self.model(board)
#                 rewards.append(reward)
#         return np.array(rewards).argmax() + 1
#
#     @staticmethod
#     def get_model_input(board, side, move):
#         board = deepcopy(board)
#         side = 1 if side == 'north' else 0
#         board = np.append(board, side)
#         board = np.append(board, move)
#         board = torch.from_numpy(board.astype(float)).unsqueeze(0).float()
#         return board
