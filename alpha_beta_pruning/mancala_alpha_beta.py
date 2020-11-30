#import sys
#sys.path.append('Users/apple/Desktop/KalahPlayer/alpha_pruning')
from mancala import Mancala
import numpy as np
class Mancala_alpha_beta(Mancala):
    def __init__(self, holes=7, stones=7, board=None):
        super().__init__(holes, stones, board)

    def is_max_node(side):
        if side == 'north':
            return False
        else:
            return True

    def get_south_scores(self):
        return self.board[self.south_store]

    def get_north_scores(self):
        return self.board[self.north_store]
    # Assume that we maximize the south side and minimize the north side
    def get_heuristics(self):
        return self.get_south_scores() - self.get_north_scores()

    def is_terminal_node(self):
        return self.has_over_half_stones("north") or \
                self.has_over_half_stones("south")

    def get_board(self):
        return self.board
    def get_store(self, side):
        return self.south_store if side == self.south else self.north_store

    def is_empty_hole(self, hole):
        #print(str(hole))
        return self.board[hole] == 0

    def get_all_possible_moves(self, side):
        move_list = []
        #print(self)
        if side == "north":
            for i in range(self.n_holes):
                if not self.is_empty_hole(i):
                    move_list.append(i)
            return move_list
        else:
            for i in range(self.n_holes):
                if not self.is_empty_hole(i + self.n_holes + 1):
                    move_list.append(i)
            return move_list


    # There we don't take several steps in a row of the same player into account,
    # because the opponent will not let that happen.
    def alpha_beta_pruning(mancala, side, alpha = -99, beta = 99, depth = 6):
        if depth == 0 or mancala.is_terminal_node():
            print("H: " + str(mancala.get_heuristics()))
            print(mancala)
            return None, mancala.get_heuristics()
        if Mancala_alpha_beta.is_max_node(side):
            optimal_value = -99
            optimal_move = None
            print("South:")
            print(mancala)
            print(mancala.get_all_possible_moves(side))
            for move in mancala.get_all_possible_moves(side):
                print("S_move: " + str(move + 1))
                print(Mancala_alpha_beta.step(mancala, side, move + 1))
                _, value = Mancala_alpha_beta.alpha_beta_pruning(Mancala_alpha_beta.step(mancala, side, move + 1),\
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
            print(mancala.get_all_possible_moves(side))
            print("---------------------")
            for move in mancala.get_all_possible_moves(side):
                print("N_move: " + str(move + 1))
                print(Mancala_alpha_beta.step(mancala, side, move + 1))
                _, value = Mancala_alpha_beta.alpha_beta_pruning(Mancala_alpha_beta.step(mancala, side, move + 1),\
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
