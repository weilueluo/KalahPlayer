from .mancalaenv import Mancala
import random
from agents.agent import Agent


def play(agent1: Agent, agent2: Agent, n_holes=7, n_stones=7):
    game = Mancala(n_holes, n_stones)
    player = random.choice(['north', 'south'])

    while not game.game_over:

        if player == 'north':
            move = agent1.get_move(game, 'north')
        else:
            move = agent2.get_move(game, 'south')
        print(game)
        print(f'Current Player: {player}, move: {move}')
        game.step(player, move)
        player = game.next_player

    if game.winner == 'north':
        winner = agent1
    elif game.winner == 'south':
        winner = agent2
    else:  # tie
        winner = None
    return winner
