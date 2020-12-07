import numpy as np

from game.mancala import Mancala


# test for the board
def boardTest(board, board_to_compare):
    boardCorrect = np.array_equal(board, board_to_compare)
    assert boardCorrect == True
    return True


# test for the msg
def msgTest(msg, msg_to_compare):
    assert msg == msg_to_compare
    return True


# test for the game board and output msg
def gameTest(msg, msg_to_compare, game, board_to_compare):
    return boardTest(game.board, board_to_compare) and msgTest(msg, msg_to_compare)


def gameEndCase(msg1, msg_to_compare1, msg2, msg_to_compare2):
    return msgTest(msg1, msg_to_compare1) and msgTest(msg2, msg_to_compare2)


game = Mancala()

# Test the start of the board
print("Start of the game board is correct: ", end=" ")
print(boardTest(game.board, np.array([7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7, 0])))

# Test a start move and the pie rule for no extra move
print("The game performs correctly for a start move: ", end=" ")
game.step('south', 1)
print(gameTest(game.next_player, "north", game, np.array([7, 7, 7, 7, 7, 7, 7, 0, 0, 8, 8, 8, 8, 8, 8, 1])))

# Test the swap case of North
game.board = np.array([7, 7, 7, 7, 7, 7, 7, 0, 0, 8, 8, 8, 8, 8, 8, 1])
print("The game performs correctly for a swap move: ", end=" ")
game.swap_side()
print(gameTest(game.next_player, "south", game, np.array([0, 8, 8, 8, 8, 8, 8, 1, 7, 7, 7, 7, 7, 7, 7, 0])))

# Test a normal move
game.board = np.array([0, 8, 8, 8, 8, 8, 8, 1, 7, 7, 7, 7, 7, 7, 7, 0])
print("The game performs correctly for a normal move: ", end=" ")
game.step('south', 2)
print(gameTest(game.next_player, "north", game, np.array([1, 8, 8, 8, 8, 8, 8, 1, 7, 0, 8, 8, 8, 8, 8, 1])))

# Test a move which will lead to an extra move
game.board = np.array([0, 8, 8, 8, 8, 8, 8, 1, 7, 7, 7, 7, 7, 7, 7, 0])
print("The game performs correctly for the extra move case: ", end=" ")
game.step('south', 1)
print(gameTest(game.next_player, "south", game, np.array([0, 8, 8, 8, 8, 8, 8, 1, 0, 8, 8, 8, 8, 8, 8, 1])))

# Test a move which will take the stones from opponent
game.board = np.array([1, 0, 9, 9, 9, 9, 9, 2, 1, 0, 11, 9, 9, 9, 9, 2])
print("The game performs correctly when need to take over opponet's stones: ", end=" ")
game.step('north', 1)
print(gameTest(game.next_player, "south", game, np.array([0, 0, 9, 9, 9, 9, 9, 12, 1, 0, 11, 9, 9, 0, 9, 2])))

# Test a move which passees two scoring wells
game.board = np.array([0, 0, 9, 9, 9, 0, 9, 12, 0, 0, 11, 9, 9, 0, 9, 12])
print("The game performs correctly when passing both scoring wells: ", end=" ")
game.step('north', 7)
print(gameTest(game.next_player, "south", game, np.array([0, 0, 9, 9, 9, 0, 0, 24, 1, 1, 12, 10, 10, 1, 0, 12])))

# Test the case the game ends if one player has no legal move
game.board = np.array([0, 0, 0, 0, 0, 0, 1, 41, 0, 0, 1, 16, 2, 2, 1, 34])
print("The game ends when one side has no moves: ", end=" ")
game.step('north', 7)
print(gameEndCase(game.game_over, True, game.winner, "south"))

# Test the case the game ends when both player has 49 stones
game.board = np.array([0, 0, 0, 0, 0, 0, 1, 48, 0, 0, 0, 0, 0, 0, 0, 49])
print("The game ends with a draw when both players have 49 stones: ", end=" ")
game.step('north', 7)
print(gameEndCase(game.game_over, True, game.winner, None))

# Test the case that the game not end when one player has 49 stones
game.board = np.array([7, 4, 0, 2, 2, 0, 1, 48, 2, 6, 1, 1, 2, 3, 0, 19])
print("The game not end when one player has 49 stones: ", end=" ")
game.step('north', 7)
print(gameTest(game.game_over, False, game, np.array([7, 4, 0, 2, 2, 0, 0, 49, 2, 6, 1, 1, 2, 3, 0, 19])))
