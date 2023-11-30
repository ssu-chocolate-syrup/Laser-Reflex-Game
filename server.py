import socket
import json
from _thread import *

from server_config import Server
from interface import PicoIO

client_sockets = []
io = PicoIO()


def push(device_id, button_id):
    data = dict(deviceID=device_id, buttonID=button_id)
    data = json.dumps(data)
    client_socket.send(data.encode())


def threaded(client_socket, addr):
    print('>> Connected by :', addr[0], ':', addr[1])
    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break
            print('>> Received from ' + addr[0], ':', addr[1], data.decode())

            client_socket.send(data)
            for client in client_sockets:
                if client != client_socket:
                    client.send(data)
        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('remove client list : ', len(client_sockets))

    client_socket.close()


print('>> Server Start with ip :', Server.HOST)
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
