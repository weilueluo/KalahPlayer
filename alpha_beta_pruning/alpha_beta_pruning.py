# import sys
# sys.path.append('Users/apple/Desktop/KalahPlayer/alpha_pruning')

from .abpmancala import ABPMancala


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
def alpha_beta_pruning(mancala, side, alpha=-99, beta=99, depth=4):
    print(f'entered alpha_beta_pruning')
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
        print(mancala.get_valid_moves(side))
        for move in mancala.get_valid_moves(side):
            print("S_move: " + str(move))
            print(ABPMancala.step(mancala, side, move))
            _, value = alpha_beta_pruning(ABPMancala.step(mancala, side, move), \
                                          mancala.get_opponent_side(side), \
                                          alpha, beta, depth - 1)
            if value > optimal_value:
                optimal_value = value
                optimal_move = move
            alpha = max(alpha, optimal_value)
            if beta <= alpha:
                print("pruning")
                break

        return optimal_move, optimal_value
    else:
        optimal_value = 99
        optimal_move = None
        print("north:")
        print(mancala)
        print(mancala.get_valid_moves(side))
        print("---------------------")
        for move in mancala.get_valid_moves(side):
            print("N_move: " + str(move))
            print(ABPMancala.step(mancala, side, move))
            _, value = alpha_beta_pruning(ABPMancala.step(mancala, side, move), \
                                          mancala.get_opponent_side(side), \
                                          alpha, beta, depth - 1)
            if value < optimal_value:
                optimal_value = value
                optimal_move = move
            beta = min(beta, optimal_value)

            if beta <= alpha:
                print(beta)
                print(alpha)
                print("pruning")
                break
        return optimal_move, optimal_value
