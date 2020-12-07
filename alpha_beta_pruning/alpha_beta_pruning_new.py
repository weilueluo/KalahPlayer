# import sys
# sys.path.append('Users/apple/Desktop/KalahPlayer/alpha_pruning')

from .abpmancala import ABPMancala
from copy import deepcopy
def is_max_node(side):
    return side == 'south'


def get_south_scores(mancala):
    return mancala.board[mancala.south_store]


def get_north_scores(mancala):
    return mancala.board[mancala.north_store]


# Assume that we maximize the south side and minimize the north side
def get_heuristics(mancala):
    return get_south_scores(mancala) - get_north_scores(mancala)


def is_terminal_node(mancala):
    return mancala.game_over


# def get_board(mancala):
#     return mancala.board

# def get_store(mancala, side):
#     return mancala.south_store if side == mancala.south else mancala.north_store

def is_empty_hole(mancala, hole):
    return mancala.board[hole] == 0


def get_all_possible_moves(mancala, side):
    return mancala.get_valid_moves(side)


# There we don't take several steps in a row of the same player into account,
# because the opponent will not let that happen.??
# ''' The reason why absolute value of alpha or beta sets to be -99 is because
#     total scores in that game is 7 * 14 = 98'''


# This function returns two things, the best move and best value got
def alpha_beta_pruning(mancala, side, alpha=-99, beta=99, depth=3):
    if is_terminal_node(mancala) and mancala.winner == 'north' and depth == 3:
        return None, -99
    if is_terminal_node(mancala) and mancala.winner == 'south' and depth == 3:
        return None, 99
        # returns none means move cannot be made because the game is finished or
        # or searching depth reaches maximum.
    if depth == 0 and is_terminal_node(mancala):
        return None, get_heuristics(mancala)
    if is_max_node(side):
        optimal_value = -99
        optimal_move = None
        for move in mancala.get_valid_moves(side):
            mancala_copy = deepcopy(mancala)
            mancala_copy.step(side, move)
            _, value = alpha_beta_pruning(mancala_copy, \
                                          mancala_copy.next_player, \
                                          alpha, beta, depth - 1)
            if value > optimal_value:
                optimal_value = value
                optimal_move = move
            alpha = max(alpha, optimal_value)
            if beta <= alpha:
                break
        return optimal_move, optimal_value
    else:
        optimal_value = 99
        optimal_move = None
        for move in mancala.get_valid_moves(side):
            mancala_copy = deepcopy(mancala)
            mancala_copy.step(side, move)
            _, value = alpha_beta_pruning(mancala_copy, \
                                          mancala_copy.next_player, \
                                          alpha, beta, depth - 1)
            if value < optimal_value:
                optimal_value = value
                optimal_move = move
            beta = min(beta, optimal_value)

            if beta <= alpha:
                break
        return optimal_move, optimal_value
