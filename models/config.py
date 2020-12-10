import random
from datetime import datetime

import numpy as np
import torch
from torch import optim
from torch.utils.tensorboard import SummaryWriter

from models.mancala import LSTMMancalaModel


class Config:
    def __init__(self,
                 model_cls=LSTMMancalaModel,
                 n_inputs=14*8,
                 n_outputs=7,
                 optimizer_cls=optim.Adam,
                 scheduler_cls=None,
                 scheduler_step_size=None,
                 scheduler_decay=None,
                 lr=0.001,
                 hidden_size=1024,
                 neuron_size=1024,
                 kernel_size=2,
                 conv_channels=5,
                 reward_discount=0.99,
                 start_epoch=0,
                 end_epochs=100000,
                 max_clip_grad=50,
                 device=torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu'),
                 seed=random.randint(1, 9999999),

                 print_interval=2000,
                 save_interval=2000,
                 evaluate_interval=2000,
                 evaluation_hook=None,
                 writer_interval=100,
                 opponent=None,

                 time_tag=datetime.today().strftime('%Y-%m-%d-%H-%M-%S'),
                 log_dir='runs',
                 model_suffix='msd',

                 n_holes=7,
                 n_stones=7,
                 max_game_length=200):

        self.model_cls = model_cls
        self.evaluation_hook = evaluation_hook
        self.optimizer_cls = optimizer_cls
        self.scheduler_cls = scheduler_cls
        self.scheduler_step_size = scheduler_step_size
        self.scheduler_decay = scheduler_decay
        self.lr = lr
        self.hidden_size = hidden_size
        self.neuron_size = neuron_size
        self.kernel_size = kernel_size
        self.conv_channels = conv_channels
        self.reward_discount = reward_discount
        self.start_epoch = start_epoch
        self.end_epochs = end_epochs
        self.max_clip_grad = max_clip_grad
        self.device = device
        self.seed = seed
        self.writer_interval = writer_interval
        self.opponent = opponent

        self.print_interval = print_interval
        self.save_interval = save_interval
        self.evaluate_interval = evaluate_interval

        self.time_tag = time_tag
        self.log_dir = log_dir
        self.model_suffix = model_suffix

        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_holes = n_holes
        self.n_stones = n_stones
        self.max_game_length = max_game_length

        self.writer = SummaryWriter(log_dir)
        self.eps = 1e-8
