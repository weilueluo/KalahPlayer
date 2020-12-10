from math import *
from decimal import *
from copy import *
from threading import *

import random
import numpy as np

import sys
sys.path.append('..')
from game.mancala import Mancala
# from alpha_beta_pruning.alpha_beta_pruning_new import alpha_beta_pruning
from alpha_beta_pruning.alpha_beta_pruning import alpha_beta_pruning

INFINITY = 1.0e400

class Node:
    def __init__(self, side:str, move:int=None, parentNode=None, game:Mancala=None):
        # the move that got us to this node - "None" for the root node
        self.move = move
        self.side = side
        self.parentNode = parentNode

        self.board = game.board
        self.childNodes = []
        self.possibleMoves = game.get_valid_moves(side)

        self.wins = 0
        self.visits = 0

        # alpha represents the balanced positions function
        # beta(ni, ni') where ni' is the number of all playouts containing move i,
        # ni stands for the number of simulations for the node considered after the i-th move
        # the value of alpha is chosen empirically
        self.alpha = 0.15

        # evalue represents the ratio of wi' to ni',
        # where wi' stands for the number of won playouts containing move i
        self.evalue = 0.0

        # whether or not the next move is still the current player
        self.again = False

        # the evaluation score of the move
        self.rvalue = 0.0

        # current node is the max, from the current player's view,
        # will be changed if the next player is no longer current player
        self.minimax = True



    def addChild(self, side, move, game:Mancala, evalue, rvalue, again):

        node = Node(side, move, parentNode=self, game=game)

        node.evalue = evalue
        node.rvalue = rvalue
        node.again = again

        if again:
            node.minimax = self.minimax
        else:
            node.minimax = not self.minimax

#         print(self.possibleMoves)
        self.possibleMoves = np.delete(self.possibleMoves, np.where(self.possibleMoves==move))
#         print(self.possibleMoves)
        self.childNodes.append(node)
        return node

    def get_opponent_side(self):
        return 'north' if self.side == 'south' else 'south'

    def update(self, win, lose):
        visits = win + lose
        self.wins += win
        self.visits += visits

    def __str__(self):
        return "[Move:" + str(self.move) + \
                "Wins/Visits:" + str(self.wins) + "/" + str(self.visits) + \
                "Side:" + self.side + \
                "]\n"

    def treeToString(self, indent, level):
        if level == 0:
            return " "
        s = self.indentToString(indent) + str(self)
        for child in self.childNodes:
            s += child.treeToString(indent+1, level-1)
        return s

    def indentToString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

#     def ChildrenToString(self):
#         s = ""
#         for child in self.childNodes:
#             s += str(child) + "\n"
#         return s

    def UCTselectChild(self):
        # UCB1 formula
        # formula = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits)

        # UCB1 RAVE formula
        formula = lambda c: (1-c.alpha)*(c.wins/c.visits)+ c.alpha*c.evalue + sqrt(2*log(self.visits)/c.visits)

        result = sorted(self.childNodes, key=formula)[-1]
        return result
