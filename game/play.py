import datetime
import os
import random
import statistics as stats
import time

from agents.agent import Agent
from .mancalaenv import Mancala


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
        self.agent1_moves = []
        self.agent2_moves = []
        self.first_move_agent = []
        self.exceed_max_game_length_count = 0
        self.start_time = time.time()
        self.end_time = None

    def _evaluate_one(self, epoch, progress, verbose=False):
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
        agent1_moves = 0
        agent2_moves = 0

        if verbose:
            print(f'game started')
            print(game)

        while not finished:
            move_time = time.time_ns()
            if player == 'north':
                move = self.agent1.get_move(game, 'north')
                self.agent1_move_time.append(time.time_ns() - move_time)
                agent1_moves += 1
            else:
                move = self.agent2.get_move(game, 'south')
                self.agent2_move_time.append(time.time_ns() - move_time)
                agent2_moves += 1

            game.step(player, move)

            if verbose:
                print(f'{player} is making a move: {move}, next_player={game.next_player} game_over={game.game_over}')
                print(game)

            player = game.next_player

            game_length += 1
            if game.game_over:
                finished = True
            elif game_length > self.max_game_length:
                self.exceed_max_game_length_count += 1
                finished = True

        self.game_times.append(time.time() - game_start_time)
        self.agent1_moves.append(agent1_moves)
        self.agent2_moves.append(agent2_moves)
        if game.winner == 'north':
            winner = self.agent1
        elif game.winner == 'south':
            winner = self.agent2
        else:  # tie
            winner = None
        self.winners.append(winner)

    def evaluate(self, agent1, agent2, n_games=100, progress=True, verbose=False):
        self._reset(agent1, agent2)
        for i in range(1, n_games + 1):
            self._evaluate_one(i, progress, verbose)
        self.end_time = time.time()
        return f'evaluation: {agent1.__class__.__name__} {self.winners.count(agent1) / len(self.winners)} ' \
               f': {self.winners.count(agent2) / len(self.winners)} {agent2.__class__.__name__}'

    @staticmethod
    def pretty_time(seconds):
        return str(datetime.timedelta(seconds=int(seconds)))

    def _agent_stats(self, agent, move_times, num_moves):
        wins = self.winners.count(agent)
        n_games = len(self.winners)
        first_move_count = self.first_move_agent.count(agent)
        stat = f'{agent.__class__.__name__}:' + os.linesep
        stat += f'\twins: {wins}/{n_games}, {wins / n_games * 100:.2f}%' + os.linesep
        stat += f'\tavg num moves: {stats.mean(num_moves)}' + os.linesep
        stat += f'\tavg move time: {int(stats.mean(move_times)) / 1e+9:.8f}s' + os.linesep
        stat += f'\tnum first move: {first_move_count}' + os.linesep

        first_move_win = sum([1 if winner == first == agent else 0
                              for winner, first in zip(self.winners, self.first_move_agent)])
        if first_move_count == 0:
            stat += f'\tfirst move wins: 0/0, nan%'
        else:
            stat += f'\tfirst move wins: {first_move_win}/{first_move_count}, {first_move_win / first_move_count * 100:.2f}%'
        return stat

    def __str__(self):
        length = 40
        string = '=' * length + os.linesep
        string += f'{self.agent1.__class__.__name__} vs {self.agent2.__class__.__name__}' + os.linesep
        string += f'holes={self.n_holes}, stones={self.n_stones}, games={len(self.winners)}' + os.linesep
        string += '-' * length + os.linesep
        string += self._agent_stats(self.agent1, self.agent1_move_time, self.agent1_moves) + os.linesep
        string += '-' * length + os.linesep
        string += self._agent_stats(self.agent2, self.agent2_move_time, self.agent2_moves) + os.linesep
        string += '-' * length + os.linesep
        string += f'draws: {self.winners.count(None)}/{len(self.winners)}, ' \
                  f'{self.winners.count(None) / len(self.winners):.2f}%' + os.linesep
        string += f'exceed: {self.exceed_max_game_length_count}/{len(self.winners)}, ' \
                  f'{self.exceed_max_game_length_count / len(self.winners):.2f}%' + os.linesep
        string += f'total time: {self.pretty_time(self.end_time - self.start_time)}' + os.linesep
        string += '=' * length + os.linesep
        return string
