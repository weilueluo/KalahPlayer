import sys
sys.path.append('parser')
from mancalaparser import Parser
sys.path.append('agents')
from alpha_pruning_agent import AlphaPruningAgent
import socket, random, parser
sys.path.append('game')
from mancala import Mancala

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('connecting to localhost 12346')
sock.bind(('localhost', 12346))
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

            if second_move:
                if msg_parser.is_swap():
                    side = "north"
                    second_move = False

            _,game_board = msg_parser.get_board()
            mancala = Mancala(7,7,game_board)
            move = AlphaPruningAgent(max_depth=5, process_depth=0, thread_depth=10).get_move(mancala,side)
            message = "MOVE;" + str(move) + "\n"
            print(message)
            server.sendall(message.encode('utf-8'))
except Exception as e:
    print("Exception:" + str(e))
finally:
    sock.close()
