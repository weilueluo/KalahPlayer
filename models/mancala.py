from torch import nn
import torch
from torch.nn import init
from torch.functional import F


def init_weights(layer):
    if isinstance(layer, nn.Linear):
        init.xavier_uniform_(layer.weight.data)
        layer.bias.data.fill_(0)


class MancalaModel(nn.Module):

    def __init__(self, n_inputs, n_outputs):
        super().__init__()

        n_neurons = 256

        def create_block(n_in, n_out, activation=True):
            block = nn.ModuleList()
            block.append(nn.Linear(n_in, n_out))
            if activation:
                block.append(nn.ReLU())
            return block

        self.blocks = nn.ModuleList()
        self.blocks.append(create_block(n_inputs, n_neurons))
        self.blocks.append(create_block(n_neurons, n_neurons))

        self.actor_block = nn.ModuleList()
        self.critic_block = nn.ModuleList()

        self.actor_block.append(create_block(n_neurons, n_outputs, activation=False))
        self.critic_block.append(create_block(n_neurons, 1, activation=False))

        self.apply(init_weights)

    def forward(self, x):
        for module in self.blocks:
            for layer in module:
                x = layer(x)
        actor = x
        critics = x
        for module in self.actor_block:
            for layer in module:
                actor = layer(actor)
        for module in self.critic_block:
            for layer in module:
                critics = layer(critics)
        return F.softmax(actor, dim=-1), critics


class MancalaModelV2(nn.Module):

    def __init__(self, n_inputs=17):
        super().__init__()

        n_neurons = 512

        def create_block(n_in, n_out, activation=True):
            block = nn.ModuleList()
            block.append(nn.Linear(n_in, n_out))
            if activation:
                block.append(nn.Dropout(p=0.1))
                block.append(nn.ReLU())
            return block

        self.blocks = nn.ModuleList()
        self.blocks.append(create_block(n_inputs, n_neurons))
        # for _ in range(1):
        #     self.blocks.append(create_block(n_neurons, n_neurons))
        self.blocks.append(create_block(n_neurons, n_neurons//2, activation=False))
        self.blocks.append(create_block(n_neurons//2, 1, activation=False))

        self.apply(init_weights)

    def forward(self, x):
        for module in self.blocks:
            for layer in module:
                x = layer(x)
        return x
