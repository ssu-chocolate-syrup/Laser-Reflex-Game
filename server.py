import socket
import json
from _thread import *

from game import LaserGame
from config import Server
from pico_interface import PicoInterface

game_instance = LaserGame()
pico_interface = PicoInterface()
client_sockets = []

def threaded(client_socket, addr):
    print('>> Connected by :', addr[0], ':', addr[1])
    
    while True:
        try:
            data = client_socket.recv(1024 * 10).decode()
            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break
            print('>> Received from ' + addr[0], ':', addr[1], data)
            data = json.loads(data)
            row, col = pico_interface.input_interface(data['deviceID'], data['buttonID'])
            if row == 0 and col == 0:
                send_data = json.dumps(game_instance.main())
            else:
                game_instance.input_mirror(row, col)
                send_data = json.dumps(game_instance.main())
            #print("data send", send_data)
            client_socket.sendall(send_data.encode())
            for client in client_sockets:
                if client != client_socket:
                    client.sendall(send_data.encode())

        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('remove client list : ', len(client_sockets))

    client_socket.close()


print('>> Server Start with ip :', Server.HOST)
# game_instance.main()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((Server.HOST, Server.PORT))
server_socket.listen()

try:
    while True:
        client_socket, addr = server_socket.accept()
        client_sockets.append(client_socket)
        start_new_thread(threaded, (client_socket, addr))
        print("참가자 수 : ", len(client_sockets))
except Exception as e:
    print('에러 : ', e)
finally:
    server_socket.close()
