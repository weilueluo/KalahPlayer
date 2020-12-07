from .mancalaenv import Mancala
import random
from agents.agent import Agent
import time
import statistics as stats
import os
import datetime


def play(agent1: Agent, agent2: Agent, n_holes=7, n_stones=7, max_game_length=200):
    game = Mancala(n_holes, n_stones)
    player = random.choice(['north', 'south'])
    game_length = 0
    finished = False

    while not finished:

        if player == 'north':
            move = agent1.get_move(game, 'north')
        else:
            move = agent2.get_move(game, 'south')
        game.step(player, move)
        player = game.next_player

        game_length += 1
        if game.game_over or game_length > max_game_length:
            finished = True

    if game.winner == 'north':
        winner = agent1
    elif game.winner == 'south':
        winner = agent2
    else:  # tie
        winner = None
    return winner


class Evaluation:

    def __init__(self, n_holes=7, n_stones=7, first_player='random', max_game_length=200):
        self.agent1 = None
        self.agent2 = None
        self.n_holes = n_holes
        self.n_stones = n_stones
        self.max_game_length = max_game_length
        self.first_player = first_player

        self._reset(None, None)

    def _reset(self, agent1, agent2):
        self.agent1 = agent1
        self.agent2 = agent2
        self.winners = []
        self.game_times = []
        self.agent1_move_time = []
        self.agent2_move_time = []
        self.first_move_agent = []
        self.exceed_max_game_length_count = 0

    def _evaluate_one(self, epoch, progress):
        game = Mancala(self.n_holes, self.n_stones)
        if progress:
            print(f'Current game: {epoch}', end='\r')

        if self.first_player == 'random':
            player = random.choice(['north', 'south'])
        else:
            player = self.first_player

        self.first_move_agent.append(self.agent1 if player == 'north' else self.agent2)

        game_length = 0
        finished = False
        game_start_time = time.time()

        while not finished:
            move_time = time.time_ns()
            if player == 'north':
                move = self.agent1.get_move(game, 'north')
                self.agent1_move_time.append(time.time_ns() - move_time)
            else:
                move = self.agent2.get_move(game, 'south')
                self.agent2_move_time.append(time.time_ns() - move_time)

            game.step(player, move)
            player = game.next_player

            game_length += 1
            if game.game_over:
                finished = True
            elif game_length > self.max_game_length:
                self.exceed_max_game_length_count += 1
                finished = True

        self.game_times.append(time.time() - game_start_time)

        if game.winner == 'north':
            winner = self.agent1
        elif game.winner == 'south':
            winner = self.agent2
        else:  # tie
            winner = None
        self.winners.append(winner)

    def evaluate(self, agent1, agent2, n_games=100, progress=True):
        self._reset(agent1, agent2)
        for i in range(1, n_games + 1):
            self._evaluate_one(i, progress)
        return self.__str__()

    @staticmethod
    def _pretty_time(seconds):
        return str(datetime.timedelta(seconds=int(seconds)))

    def _agent_stats(self, agent, move_times):
        wins = self.winners.count(agent)
        n_games = len(self.winners)
        first_move_count = self.first_move_agent.count(agent)
        stat = f'{agent.__class__.__name__}:' + os.linesep
        stat += f'\twins: {wins}/{n_games}, {wins / n_games * 100:.2f}%' + os.linesep
        stat += f'\tavg move time: {int(stats.mean(move_times))/1e+9:.8f}s' + os.linesep
        stat += f'\tnum first move: {first_move_count}' + os.linesep

        first_move_win = sum([1 if winner == first == agent else 0
                              for winner, first in zip(self.winners, self.first_move_agent)])
        stat += f'\tfirst move wins: {first_move_win}/{first_move_count}, {first_move_win/first_move_count*100:.2f}%'
        return stat

    def __str__(self):
        length = 40
        print('=' * length)
        print(f'{self.agent1.__class__.__name__} vs {self.agent2.__class__.__name__}')
        print(f'holes={self.n_holes}, stones={self.n_stones}, games={len(self.winners)}')
        print('-' * length)
        print(self._agent_stats(self.agent1, self.agent1_move_time))
        print('-' * length)
        print(self._agent_stats(self.agent2, self.agent2_move_time))
        print('-' * length)
        print(f'draws: {self.winners.count(None)}/{len(self.winners)}, '
              f'{self.winners.count(None) / len(self.winners):.2f}%')
        print(f'exceed: {self.exceed_max_game_length_count}/{len(self.winners)}, '
              f'{self.exceed_max_game_length_count / len(self.winners):.2f}%')
        print('=' * length)
