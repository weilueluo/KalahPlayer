# import sys
# sys.path.append('Users/apple/Desktop/KalahPlayer/alpha_pruning')

import functools
import sys
from copy import deepcopy
from multiprocessing import Pool as ProcessPool
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool
from operator import lt, gt

from game.mancala import Mancala


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


# There we don't take several steps in a row of the same player into account,
# because the opponent will not let that happen.??
# ''' The reason why absolute value of alpha or beta sets to be -99 is because
#     total scores in that game is 7 * 14 = 98'''


def alpha_beta_pruning(mancala, side, max_depth=3, max_process_depth=0, max_threading_depth=0):
    max_return = mancala.n_holes * mancala.n_stones + 1
    return _alpha_beta_pruning(mancala=mancala,
                               side=side,
                               seq_num=0,
                               alpha=-max_return,
                               beta=max_return,
                               max_depth=max_depth,
                               curr_depth=max_depth,
                               process_depth=max_process_depth,
                               threading_depth=max_threading_depth)[0]


def get_next_mancala(mancala, side, move):
    mancala_copy = Mancala(board=deepcopy(mancala.board))
    mancala_copy.step(side, move)
    return mancala_copy


def _alpha_beta_pruning_mp(args, alpha, beta, curr_depth, process_depth, threading_depth):
    mancala, side, seq = args
    return _alpha_beta_pruning(mancala=mancala, side=side, seq_num=seq,
                               alpha=alpha, beta=beta, curr_depth=curr_depth,
                               process_depth=process_depth, threading_depth=threading_depth)


# This function returns two things, the best move and best value got
def _alpha_beta_pruning(mancala, side, seq_num, alpha=-99, beta=99, max_depth=3,
                        curr_depth=3, process_depth=0, threading_depth=0):
    # base case
    if curr_depth == 0 or is_terminal_node(mancala):
        return None, get_heuristics(mancala), seq_num
    # step case
    max_return = mancala.n_holes * mancala.n_stones + 1
    if is_max_node(side):
        optimal_value = -max_return
        order = max
        comparator = gt
    else:
        optimal_value = max_return
        order = min
        comparator = lt

    optimal_move = None
    valid_moves = mancala.get_valid_moves(side)

    if process_depth > 0 or threading_depth > 0:
        if process_depth > 0:
            pool_type = ProcessPool
            process_depth -= 1
            processes = cpu_count()
        else:
            pool_type = ThreadPool
            threading_depth -= 1
            processes = 2
        next_mancalas = []
        for i, move in enumerate(valid_moves):
            mancala_copy = get_next_mancala(mancala, side, move)
            next_mancalas.append((mancala_copy, mancala_copy.next_player, i))
        partial_abp = functools.partial(_alpha_beta_pruning_mp, alpha=alpha, beta=beta, curr_depth=curr_depth - 1,
                                        process_depth=process_depth, threading_depth=threading_depth)
        for _, value, i in pool_type(processes).imap_unordered(partial_abp, next_mancalas):
            if comparator(value, optimal_value):
                optimal_value = value
                optimal_move = valid_moves[i]
            alpha = order(alpha, optimal_value)
            if beta <= alpha:
                break
        return optimal_move, optimal_value, seq_num

    for move in valid_moves:
        mancala_copy = get_next_mancala(mancala, side, move)
        _, value, _ = _alpha_beta_pruning(mancala=mancala_copy,
                                          side=mancala_copy.next_player,
                                          seq_num=seq_num,
                                          alpha=alpha,
                                          beta=beta,
                                          max_depth=max_depth,
                                          curr_depth=curr_depth - 1)
        if comparator(value, optimal_value):
            optimal_value = value
            optimal_move = move
        alpha = order(alpha, optimal_value)
        if beta <= alpha:
            break
    return optimal_move, optimal_value, seq_num
