## CLIENT ##
# 테스트1 파일입니다 이걸실행하면 너도 오류를 마구마구 고칠 수있다구
import json
import time
import struct
import socket
from _thread import *

from pico_interface import PicoInterface
from config import Server, Wifi
from return_class import ReturnClass

HOST = input('서버에 출력되는 IP주소를 입력하세요')
PORT = 9999

print('>> connecting socket')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

test = [[6, 3],
        [5, 7],
        [6, 6],
        [5, 7],
        [6, 6],
        [5, 7],
        [3, 6],
        [5, 7],
        [1, 3],
        [5, 7],
        [1, 3], ]


def input_mirror(row, col):
    device_id, button = PicoInterface.output_interface(row, col)
    message = ReturnClass(_color_type=None, _device_id=device_id, _button_id=button)
    message_json = json.dumps(message.get_convert_dict()).encode()
    client_socket.sendall(struct.pack('!I', len(message_json)))
    client_socket.sendall(message_json)


def recv_all(client_socket, byte_size):
    data = b''
    while len(data) < byte_size:
        packet = client_socket.recv(byte_size - len(data))
        if not packet:
            return None
        data += packet
    return data


def recv_data(client_socket):
    while True:
        raw_message_len = recv_all(client_socket, 4)
        message_len = struct.unpack('!I', raw_message_len)[0]
        data = recv_all(client_socket, message_len).decode()
        data = [ReturnClass().get_convert_return_class(item) for item in json.loads(data)]
        return data


start_new_thread(recv_data, (client_socket,))
print('>> Connect Server')
print('test1_start')

for i in test:
    input_mirror(i[0], i[1])
    time.sleep(1)

client_socket.close()
