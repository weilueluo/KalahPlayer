import numpy as np


class Parser:
    def __init__(self, server_text):
        self.msg = server_text

    def str_to_num(self, string):
        return [int(str) for str in string]

    def msg_to_board(self, msg):
        board = self.str_to_num(msg)
        return '{:2d}  {}\n    {}  {}'.format(
            board[7],
            board[0:7][::-1],
            board[8:15],
            board[15]
        )

    def ini_board(self):
        ini_board = np.full(16, 7)
        ini_board[7] = 0
        ini_board[15] = 0
        str_board = self.msg_to_board(ini_board)
        return str_board, ini_board

    def get_board(self):
        #         print(self.msg)
        global next_move
        global str_board
        global board
        global moveswap
        if self.is_start():
            str_board, board = self.ini_board()
            next_move = 'YOU'
        #             print(next_move)
        elif self.is_state_change():
            change_str, moveswap, board, side = self.msg.split(';')
            if moveswap.isdigit():  # move state
                print(next_move, ' moved ', moveswap, 'th hole.')
            else:  # swap state
                print('The board has been swapped.')

            next_move = side
            print('The board after the state change is:')
            str_board = self.msg_to_board(board.split(','))
            board = self.str_to_num(board.split(','))
        return str_board, board

    def winner(self, board):
        n_score = board[7]
        s_score = board[-1]
        text = 'no winner'
        if n_score > s_score:
            text = 'You lose!'
        elif n_score == s_score:
            text = 'It is a draw!'
        else:
            text = 'You win!'
        return text

    def is_state_change(self):
        return self.msg.startswith('CHANGE') or self.msg.endswith('YOU') or self.msg.endswith('OPP')

    def is_start(self):
        return self.msg.startswith('START')

    def is_our_turn(self):
        return self.is_start() or self.msg.endswith('YOU')

    def is_end(self):
        return self.msg == 'END'

    def is_over(self):
        return self.msg.endswith('END') or self.msg.endswith('E')

    def not_recognizable(self):
        return not self.is_start() and not self.is_state_change() and not self.is_end()

    def __str__(self):
        return self.msg
