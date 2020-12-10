from math import *
from decimal import *
from copy import *
from threading import *

import random
import numpy as np

import sys
from game.mancala import Mancala
from .node import Node
# from alpha_beta_pruning.alpha_beta_pruning_new import alpha_beta_pruning
from alpha_beta_pruning.alpha_beta_pruning import alpha_beta_pruning

class MCTS:


    INFINITY = float('inf')

    def winlose(side, game:Mancala):
        # print the heuristics of the current side

        s1 =0.0
        s2 =0.0

        # current player wins
        if game.has_over_half_stones(side):
            return INFINITY

        # current player loses
        if game.has_over_half_stones(game.get_opponent_side(side)):
            return -INFINITY

        # score of current player
        s1 = game.board[game.get_store(side)]

        # score of other player
        s2 = game.board[game.get_store(game.get_opponent_side(side))]

        # total score
        total = float(game.n_stones * game.n_holes * 2)

        return ((s1 - s2) / total + sqrt(s1) / sqrt(total)) /2

    def score(side, game:Mancala):
        # print the current score of a side, which is from -1 to 1(including -1 and 1)


        s1 = 0.0 ### all scores from base and this side's stones
        s2 = 0.0 ### all scores from opposite base and opposite stones
        ######################################################################################
        ### should set weight to scores for different side ###################################
        ######################################################################################
        s1 += np.sum(game.board[game.get_start_hole(side):game.get_store(side)])
        s1 += game.board[game.get_store(side)]

        if game.has_over_half_stones(side):
            return 1

        s2 += np.sum(game.board[game.get_start_hole(game.get_opponent_side(side)):game.get_store(game.get_opponent_side(side))])
        s2 += game.board[game.get_store(game.get_opponent_side(side))]


        if game.has_over_half_stones(game.get_opponent_side(side)):
            return -1

        total = float(game.n_stones * game.n_holes * 2)
        return ((s1-s2) / total + sqrt(s1)/sqrt(total/2)) /2

    def catchMove(side, game:Mancala, move):
        # whether exists a move, that can catch the stones opposite to an empty hole
        # returns a boolean of availability of catching and the move to catch it

        ### note: if there are multiple catchMove exists, function will take the first detected one.
        ### if there is no possible catch, return False, -1
        ### example output:
        ###
        ###  3  [ 10  10  10  10   2   0   1]
        ###     [  1  10   8   8   8   8   8]  1
        ###     Traps for:south hole=6 oppoHole=1
        ###     True, 0
        ###
        ### this means there is a catchMove for north, to move the 'oppoHole' hole
        ### so south now needs to move the 'hole'


        ### self holes, normally is game.board[0:7]
        selfHoles = game.board[game.get_start_hole(side):game.get_store(side)]
    #     print(selfHoles)
        ### opponent's holes, normally is game.board[8:15]
        oppoHoles = game.board[game.get_start_hole(game.get_opponent_side(side)):game.get_store(game.get_opponent_side(side))]
    #     print(oppoHoles)

        if selfHoles[move-1] > 1 and oppoHoles[len(oppoHoles)-move] == 0:
    #         print(True)
            for i in range(len(oppoHoles)):

                if oppoHoles[i] == 0:
                    continue

                ### first array
                if oppoHoles[i] + i <= 6:
                    if oppoHoles[i] + i == len(oppoHoles)-move:
    #                     print("Traps for:"+str(side)+" hole="+str(move)+" oppoHole="+str(i+1))
                        return True, i
                ### second array
                elif oppoHoles[i] + i >= 15:
                    if oppoHoles[i] + i - 15 == len(oppoHoles)-move:
    #                     print("Traps for:"+str(side)+" hole="+str(move)+" oppoHole="+str(i+1))
                        return True, i
        return False, -1

    def get_again(game:Mancala, side):
        return game.next_player == side

    def get_opponent_side(side):
        return 'north' if side == 'south' else 'south'

    def UCT(rootGame:Mancala, side:str):

        ### rootgame: the game Mancala
        ### side: the player(south or north)

        ### Conduct a UCT search for a number of iterations starting from rootstate.
        ### Return the best move from the rootstate.


        rootNode = Node(game = rootGame, side = side)
        rootPlayer = deepcopy(side)

        ### self holes, normally is game.board[8:15]
        selfHoles = rootGame.get_holes(side)
    #     print(selfHoles)
        ### opponent's holes, normally is game.board[0:7]
        oppoHoles = rootGame.get_holes(rootGame.get_opponent_side(side))
    #     print(oppoHoles)

    #     print('UCT Starts!!!!!!!!!!')
    #     print(rootGame)
        i = 0
        while True:

            print(f'MCTS Processing: ' + str(i), end='\r')

            node = rootNode
            game = deepcopy(rootGame)


            ### return If there is a win move found only when root node is fully exploited
            ### assume the mamimum-visits is 100, as there are only 98 stones
            if len(rootNode.childNodes) > 0 and len(node.childNodes) > 0 and rootNode.visits == 100:

                for child in rootNode.childNodes:

                    if child.rvalue == 1:
    #                     print(f'The final move is ', child.move)
                        return child.move

                    if child.again:
                        move, _ = alpha_beta_pruning(rootGame, rootPlayer, depth=3)
    #                     print("Again child.Move="+str(child.move)+" Alpha-Beta Depth=3 Move="+str(move))
    #                     print(f'The final move is ', move)
                        return move

                    catch_possible, catch_move = MCTS.catchMove(rootPlayer, rootGame, child.move)
                    ### if we can catch a move, then we do that move
                    if catch_possible:
    #                     print(f'The final move is ', child.move)
                        return child.move

                    catch_possible, catch_move = MCTS.catchMove(MCTS.get_opponent_side(rootPlayer), rootGame, child.move)
                    ### if opponent can catch our move, then we do the move which prevents that
                    if catch_possible:
    #                     print(f'The final move is ', catch_move)
                        return catch_move

                final_move = sorted(rootNode.childNodes, key = lambda c: c.visits)[-1].move
    #             print(f'The final move is ', final_move)
                return final_move



            ##### SELECT #####
            while node.possibleMoves.size != 0 and len(node.childNodes) > 0: # node is fully expanded and non-terminal
                node = node.UCTselectChild()
                game.step(node.side, node.move)
    #             print("Select Start Player:"+str(node.player.num)+" Move:"+str(node.move))



            ##### Expand #####
            if node.possibleMoves.size > 0:

                move = random.choice(node.possibleMoves)
                game.step(node.side, move)
                again = MCTS.get_again(game, node.side)
    #             print("Expand make move Player:"+str(node.player.num)+" Move:"+str(m))

                if again:
                    nodePlayer = node.side
                else:
                    nodePlayer = node.get_opponent_side()
    #             print("Expand AddChild Player:"+str(nodeplayer)+" Move:"+str(m))

                evalue = MCTS.score(rootPlayer, game)
                rvalue = MCTS.winlose(rootPlayer, game)

                node = node.addChild(nodePlayer, move, game, evalue, rvalue, again)


            ##### RollOut #####
            while not game.game_over:

                if game.has_over_half_stones(side) or game.has_over_half_stones(game.get_opponent_side(side)):
                    break

                ### temporary using minimax
                move, _ = alpha_beta_pruning(game, nodePlayer, depth=3)

                game.step(nodePlayer, move)
                again = MCTS.get_again(game, nodePlayer)
                if not again:
                    nodePlayer = MCTS.get_opponent_side(nodePlayer)

            ##### BackPropagate #####
            if game.board[game.get_store(rootPlayer)] >= game.board[game.get_store(game.get_opponent_side(rootPlayer))]:
                win = 1
                lose = 0
            else:
                win = 0
                lose = 1

            while node != None: # backpropagate from the expanded node and work back to the root node

                node.update(win, lose) # update the wins and losses

                if len(node.childNodes) > 0:

                    rvalue = 0.0 # initial each child has 0 score
                    loseTime = 0 # total number of losing

                    # an iter-changable boolean, represents the final state of win
                    # if number of wins outweigh number of losses, hasWin is True
                    hasWin = False

                    # an iter-changable boolean, represents the final state of lose
                    # if number of losses outweigh number of wins, hasLose is True
                    hasLose = False

                    # a final decision boolean, represents the final state of child's performance
                    # if number of losses is the same as number of wins,
                    # hasAverage is True
                    hasAverage = False

                    for child in node.childNodes:

                        if child.rvalue == -MCTS.INFINITY:
                            hasLose = True
                            loseTime += 1

                        if child.rvalue == MCTS.INFINITY:
                            hasWin = True
                            loseTime -= 1

                        if child.rvalue != MCTS.INFINITY and  child.rvalue != -MCTS.INFINITY:
                            hasAverage = True
                            rvalue += child.rvalue

                    if hasWin:
                        node.rvalue = MCTS.INFINITY
                    elif hasLose and not hasWin and not hasAverage:
                        node.rvalue = -MCTS.INFINITY
                    elif hasLose and hasAverage:
                        node.rvalue = (rvalue - loseTime) / len(node.childNodes)
                    else:
                        node.rvalue = rvalue / len(node.childNodes)

                    if node.minimax:
                        node.evalue = sorted(node.childNodes, key = lambda c: c.evalue)[-1].evalue
                    else:
                        node.evalue = sorted(node.childNodes, key = lambda c: c.evalue)[0].evalue

                node = node.parentNode

            i += 1
