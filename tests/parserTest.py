class ParserTest:

    def __init__(self):
        self.text = ''      # text from server
        self.lose = 'You lose!'   #  result of lose
        self.draw = 'It is a draw!'    # result of draw
        self.win = 'You win!'   # result of win
        self.swap = 'The board has been swapped.'   # result of swapping
        self.no_swap = 'There is no swap.'  # result of no swapping

    def start_test(self):
        text = 'START:SOUTH'
        msg = Parser(text)
        assert not msg.is_state_change() and msg.is_our_turn() and not msg.is_over() and not msg.is_end()
        assert not msg.not_recognizable()
        assert msg.is_start()
        assert str(msg) == text

    def move_test(self):
        text = 'CHANGE;3;8,8,7,7,7,7,7,0,7,7,0,8,8,8,8,1;OPP'
        msg = Parser(text)
        print_board, board, result_msg = msg.get_board()
        assert not msg.is_start() and not msg.is_our_turn() and not msg.is_over() and not msg.is_end()
        assert result_msg == self.no_swap and not msg.not_recognizable()
        assert msg.is_state_change() and msg.winner(board) == self.win
        assert str(msg) == text

    def swap_test(self):
        text = 'CHANGE;SWAP;8,8,8,8,0,7,7,1,8,8,7,7,7,7,7,0;YOU'
        msg = Parser(text)
        print_board, board, result_msg = msg.get_board()
        assert not msg.is_start() and not msg.is_over() and not msg.is_end() and not msg.not_recognizable()
        assert msg.is_state_change() and msg.winner(board) == self.lose and msg.is_our_turn()
        assert result_msg == self.swap
        assert str(msg) == text

    def over_win_test(self):
        text = 'CHANGE;1;0,0,0,0,0,0,0,25,0,0,0,0,0,0,0,73;END'
        msg = Parser(text)
        print_board, board, result_msg = msg.get_board()
        assert not msg.is_start() and not msg.is_end() and not msg.not_recognizable()
        assert msg.is_over() and msg.is_state_change() and msg.winner(board) == self.win and not msg.is_our_turn()
        assert result_msg == self.no_swap
        assert str(msg) == text

    def over_lose_test(self):
        text = 'CHANGE;1;0,0,0,0,0,0,0,73,0,0,0,0,0,0,0,25;END'
        msg = Parser(text)
        print_board, board, result_msg = msg.get_board()
        assert not msg.is_start() and not msg.is_end() and not msg.not_recognizable()
        assert msg.is_over() and msg.is_state_change() and msg.winner(board) == self.lose and not msg.is_our_turn()
        assert result_msg == self.no_swap
        assert str(msg) == text

    def end_test(self):
        text = 'END'
        msg = Parser(text)
        assert msg.is_end() and msg.is_over()
        assert not msg.is_start() and not msg.is_state_change() and not msg.not_recognizable() and not msg.is_our_turn()
        assert str(msg) == text

    def wrong_message_test(self):
        text = 'aaaaabbbbb'
        msg = Parser(text)
        assert msg.not_recognizable() and not msg.is_start() and not msg.is_state_change() and not msg.is_our_turn()
        assert not msg.is_end() and not msg.is_over()
        assert str(msg) == text

    def runall(self):
        for obj in dir(ParserTest()):
            if obj.endswith('test'):
                getattr(ParserTest(), obj)()  # run all tests
