from torch import nn
import torch
from torch.nn import init
from torch.functional import F


def init_weights(layer):
    if isinstance(layer, nn.Linear):
        init.xavier_uniform_(layer.weight.data)
        layer.bias.data.fill_(0)


class MancalaModel(nn.Module):

    def __init__(self, n_inputs, n_outputs, hidden_size):
        super().__init__()

        n_neurons = 1024

        def create_block(n_in, n_out, activation=True):
            block = [nn.Linear(n_in, n_out)]
            if activation:
                block.append(nn.ReLU())
            return nn.Sequential(*block)

        self.blocks = []
        self.blocks.append(create_block(n_inputs, n_neurons))
        self.blocks.append(nn.Dropout(p=0.2))
        self.blocks.append(create_block(n_neurons, hidden_size))

        self.lstm = nn.LSTMCell(input_size=hidden_size, hidden_size=hidden_size)

        self.actor_block = []
        self.critic_block = []

        self.actor_block.append(create_block(hidden_size, n_outputs, activation=False))
        self.critic_block.append(create_block(hidden_size, 1, activation=False))

        self.blocks = nn.Sequential(*self.blocks)
        self.actor_block = nn.Sequential(*self.actor_block)
        self.critic_block = nn.Sequential(*self.critic_block)

        self.apply(init_weights)

    def forward(self, x, h):
        x = self.blocks(x)
        hx, cx = self.lstm(x, h)
        actor = critics = hx
        actor = self.actor_block(actor)
        critics = self.critic_block(critics)
        return F.softmax(actor, dim=-1), critics, (hx, cx)


# Simple Agent 100% model
# class MancalaModel(nn.Module):
#
#     def __init__(self, n_inputs, n_outputs, hidden_size):
#         super().__init__()
#
#         n_neurons = 1024
#
#         def create_block(n_in, n_out, activation=True):
#             block = [nn.Linear(n_in, n_out)]
#             if activation:
#                 block.append(nn.ReLU())
#             return nn.Sequential(*block)
#
#         self.blocks = []
#         self.blocks.append(create_block(n_inputs, n_neurons))
#         self.blocks.append(nn.Dropout(p=0.2))
#         self.blocks.append(create_block(n_neurons, hidden_size))
#
#         self.lstm = nn.LSTMCell(input_size=hidden_size, hidden_size=hidden_size)
#
#         self.actor_block = []
#         self.critic_block = []
#
#         self.actor_block.append(create_block(hidden_size, n_outputs, activation=False))
#         self.critic_block.append(create_block(hidden_size, 1, activation=False))
#
#         self.blocks = nn.Sequential(*self.blocks)
#         self.actor_block = nn.Sequential(*self.actor_block)
#         self.critic_block = nn.Sequential(*self.critic_block)
#
#         self.apply(init_weights)
#
#     def forward(self, x, h):
#         x = self.blocks(x)
#         hx, cx = self.lstm(x, h)
#         actor = critics = hx
#         actor = self.actor_block(actor)
#         critics = self.critic_block(critics)
#         return F.softmax(actor, dim=-1), critics, (hx, cx)