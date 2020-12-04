from .mancalaenv import Mancala
import random
from agents.agent import Agent


def play(agent1: Agent, agent2: Agent, n_holes=7, n_stones=7, max_game_length=150):
    game = Mancala(n_holes, n_stones)
    player = random.choice(['north', 'south'])
    game_length = 0
    finished = False

    while not finished:

        if player == 'north':
            move = agent1.get_move(game, 'north')
        else:
            move = agent2.get_move(game, 'south')
        # print(game)
        # print(f'Current Player: {player}, move: {move}')
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
