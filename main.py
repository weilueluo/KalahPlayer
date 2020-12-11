import sys
sys.path.append('parser')
from mancalaparser import Parser
sys.path.append('agents')
from alpha_pruning_agent import AlphaPruningAgent
import socket, random, parser
sys.path.append('game')
from mancala import Mancala
from copy import deepcopy
import random
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('connecting to localhost 12345')
sock.bind(('localhost', 12345))
sock.listen(1)
server, address = sock.accept()

def receive_line(client):
    buffer = bytearray()
    while True:
        data = client.recv(4)
        buffer.extend(data)
        if b'\n' in data:
            break
        if not data:
            return None

    return buffer

side = None
first_move = False
second_move = False

try:
    has_win = False
    while True:
        byte_stream = receive_line(server)
        if byte_stream == None:
            break
        else:
            server_text = byte_stream.decode('utf-8').rstrip()
        msg_parser = Parser(server_text)

        if msg_parser.is_start():
            side = msg_parser.get_side()
            first_move = True

        if msg_parser.is_end():
            break

        if has_win and msg_parser.is_our_turn():
            _,game_board = msg_parser.get_board()
            mancala = Mancala(7,7,game_board)
            valid_moves = mancala.get_valid_moves(side)
            move = random.choice(valid_moves)
            #print("has win")
            message = "MOVE;" + str(move) + "\n"
            server.sendall(message.encode('utf-8'))
            continue



        if first_move:
            if side == 'north' and msg_parser.is_our_turn():
                message = "SWAP\n"
                side = "south"
                server.sendall(message.encode('utf-8'))
                first_move = False
            elif side == 'south' and msg_parser.is_start():
                message = "MOVE;1\n"
                server.sendall(message.encode('utf-8'))
                first_move = False
                second_move = True

        elif msg_parser.is_our_turn():
            #print(side)
            if second_move:
                if msg_parser.is_swap():
                    side = "north"
                    second_move = False

            _,game_board = msg_parser.get_board()
            mancala = Mancala(7,7,game_board)
            valid_moves = mancala.get_valid_moves(side)
            #print(valid_moves)
            for move in valid_moves:
                mancala_copy = deepcopy(mancala)
                mancala_copy.step(side, move)
                if mancala_copy.winner == side:
                    message = "MOVE;" + str(move) + "\n"
                    server.sendall(message.encode('utf-8'))
                    has_win = True
                    break
            if has_win:
                continue
            move = AlphaPruningAgent(max_depth=4, process_depth=0, thread_depth=0).get_move(mancala,side)
            message = "MOVE;" + str(move) + "\n"
            print(message)
            server.sendall(message.encode('utf-8'))
except Exception as e:
    print("Exception:" + str(e))
finally:
    sock.close()
