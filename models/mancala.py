from torch import nn
from torch.nn import init


def init_weights(layer):
    if isinstance(layer, nn.Linear):
        init.xavier_uniform_(layer.weight.data)
        layer.bias.data.fill_(0)


class MancalaModel(nn.Module):

    def __init__(self, n_inputs, n_outputs, hidden_size, neuron_size):
        super().__init__()

        n_neurons = neuron_size

        def create_block(n_in, n_out, activation=True):
            block = [nn.Linear(n_in, n_out)]
            if activation:
                block.append(nn.ReLU())
            return nn.Sequential(*block)

        self.blocks = []
        self.blocks.append(create_block(n_inputs, n_neurons))
        self.blocks.append(nn.Dropout(p=0.2))
        self.blocks.append(create_block(n_neurons, n_neurons))
        self.blocks.append(create_block(n_neurons, hidden_size))

        self.lstm = nn.LSTMCell(input_size=hidden_size, hidden_size=hidden_size)

        self.actor_block = []
        self.critic_block = []

        self.actor_block.append(create_block(hidden_size, hidden_size))
        self.actor_block.append(create_block(hidden_size, n_outputs, activation=False))
        self.critic_block.append(create_block(hidden_size, hidden_size))
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
        return actor, critics, (hx, cx)


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


import torch


class Normalization(nn.Module):
    def __init__(self, eps):
        super().__init__()
        self.eps = eps

    def forward(self, x: torch.Tensor):
        x -= torch.min(x, dim=1, keepdim=True)[0]
        x /= torch.max(x, dim=1, keepdim=True)[0] + self.eps
        return x


class LSTMMancalaModel(nn.Module):

    def __init__(self, n_inputs, n_outputs, hidden_size=512, neuron_size=512):
        super().__init__()

        def create_block(n_in, n_out, activation=True):
            block = [nn.Linear(n_in, n_out)]
            if activation:
                block.append(nn.LeakyReLU())
            # if normalization:
            #     block.append(Normalization(1e-6))
            return nn.Sequential(*block)

        self.linear_block = []
        self.reduce_block = []
        self.actor_block = []
        self.critic_block = []

        # block 1: linear
        self.linear_block.append(create_block(n_inputs, neuron_size))
        self.linear_block.append(nn.Dropout(p=0.2))
        self.linear_block.append(create_block(neuron_size, hidden_size))

        # block 3: LSTM
        self.lstm = nn.LSTMCell(input_size=hidden_size, hidden_size=hidden_size)

        # block 4: reduce size
        self.reduce_block.append(create_block(hidden_size, hidden_size // 2))

        # block 5: actor and critic
        # self.actor_block.append(create_block(hidden_size // 2, hidden_size // 4, normalization=False))
        self.actor_block.append(create_block(hidden_size // 2, n_outputs, activation=False))
        # self.critic_block.append(create_block(hidden_size // 2, hidden_size // 4, normalization=False))
        self.critic_block.append(create_block(hidden_size // 2, 1, activation=False))

        self.linear_block = nn.Sequential(*self.linear_block)
        self.reduce_block = nn.Sequential(*self.reduce_block)
        self.actor_block = nn.Sequential(*self.actor_block)
        self.critic_block = nn.Sequential(*self.critic_block)

        self.apply(init_weights)

    def forward(self, x, h):
        x = self.linear_block(x)
        hx, cx = self.lstm(x, h)
        x = self.reduce_block(hx)
        actor = critics = x
        actor = self.actor_block(actor)
        critics = self.critic_block(critics)
        return actor, critics, (hx, cx)
