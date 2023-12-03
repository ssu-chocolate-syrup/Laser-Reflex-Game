## CLIENT ##
#컴퓨터에서 서버와 통신할수있는 테스트 파일입니다.
import json
import time
import struct
import socket
from _thread import *

HOST = '172.20.10.7' ## server에 출력되는 ip를 입력해주세요 ##
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        print("recive : ", repr(data.decode()))


start_new_thread(recv_data, (client_socket,))
print('>> Connect Server')

while True:
    device_id=input('device id를 입력하시오')
    button=input('button을 입력하시오')
    message = dict(d=int(device_id),
                   b=int(button))
    message_json = json.dumps(message).encode()
    client_socket.sendall(struct.pack('!I', len(message_json)))
    client_socket.sendall(message_json)

client_socket.close()
