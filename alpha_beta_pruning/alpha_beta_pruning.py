#import sys
#sys.path.append('Users/apple/Desktop/KalahPlayer/alpha_pruning')
from mancala import Mancala
import numpy as np
def is_max_node(side):
    if side == 'north':
        return False
    else:
        return True

def get_south_scores(mancala):
    return mancala.board[mancala.south_store]

def get_north_scores(mancala):
    return mancala.board[mancala.north_store]
# Assume that we maximize the south side and minimize the north side
def get_heuristics(mancala):
    return get_south_scores(mancala) - get_north_scores(mancala)

def is_terminal_node(mancala):
    return mancala.has_over_half_stones("north") or \
            mancala.has_over_half_stones("south")

def get_board(mancala):
    return mancala.board

# def get_store(mancala, side):
#     return mancala.south_store if side == mancala.south else mancala.north_store

def is_empty_hole(mancala, hole):
    return mancala.board[hole] == 0

def get_all_possible_moves(mancala, side):
    move_list = []
    #print(self)
    if side == "north":
        for i in range(mancala.n_holes):
            if not is_empty_hole(mancala,i):
                move_list.append(i + 1)
        return move_list
    else:
        for i in range(mancala.n_holes):
            if not is_empty_hole(mancala, i + mancala.n_holes + 1):
                #returns i + 1 because move ranges from 1 to 7
                move_list.append(i + 1)
        return move_list


# There we don't take several steps in a row of the same player into account,
# because the opponent will not let that happen.??
''' The reason why absolute value of alpha or beta sets to be -99 is because
    total scores in that game is 7 * 14 = 98'''
#This function returns two things, the best move and best value got
def alpha_beta_pruning(mancala, side, alpha = -99, beta = 99, depth = 4):
    if depth == 0 or is_terminal_node(mancala):
        print("H: " + str(get_heuristics(mancala)))
        print(mancala)
        # returns none means move cannot be made because the game is finished or
        # or searching depth reaches maximum.
        return None, get_heuristics(mancala)
    if is_max_node(side):
        optimal_value = -99
        optimal_move = None
        print("South:")
        print(mancala)
        print(get_all_possible_moves(mancala,side))
        for move in get_all_possible_moves(mancala, side):
            print("S_move: " + str(move))
            print(Mancala.step(mancala, side, move))
            _, value = alpha_beta_pruning(Mancala.step(mancala, side, move),\
                                            mancala.get_opponent_side(side), \
                                            alpha, beta, depth-1)
            if value > optimal_value:
                optimal_value = value
                optimal_move = move
            alpha = max(alpha, optimal_move)
            if beta <= alpha:
                print("pruning")
                break

        return optimal_move, optimal_value
    else:
        optimal_value = 99
        optimal_move = None
        print("north:")
        print(mancala)
        print(get_all_possible_moves(mancala, side))
        print("---------------------")
        for move in get_all_possible_moves(mancala, side):
            print("N_move: " + str(move))
            print(Mancala.step(mancala, side, move))
            _, value = alpha_beta_pruning(Mancala.step(mancala, side, move),\
                                                  mancala.get_opponent_side(side), \
                                                  alpha, beta, depth-1)
            if value < optimal_value:
                optimal_value = value
                optimal_move = move
            beta = min(beta, optimal_move)

            if beta <= alpha:
                print(beta)
                print(alpha)
                print("pruning")
                break
        return optimal_move, optimal_value
