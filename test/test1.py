## CLIENT ##
#테스트1 파일입니다 이걸실행하면 너도 오류를 마구마구 고칠 수있다구
import json
import time
import struct
import socket
from _thread import *
from pico_interface import PicoInterface
from config import Server,WIfI
host=input('서버에 출력되는 IP주소를 입력하세요')
HOST = host 
PORT = 9999

print('>> connecting socket')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

test=[[6,3],
      [5,7],
      [6,6],
      [5,7],
      [6,6],
      [5,7],
      [3,6],
      [5,7],
      [1,3],
      [5,7],
      [1,3],]
      

def simul(row,col):
    device_id,button = PicoInterface.output_interface(row,col)
    message = dict(d=int(device_id),
                       b=int(button))
    message_json = json.dumps(message).encode()
    client_socket.sendall(struct.pack('!I', len(message_json)))
    client_socket.sendall(message_json)
def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        print("recive : ", repr(data.decode()))


start_new_thread(recv_data, (client_socket,))
print('>> Connect Server')
print('test1_start')
for i in test:
    simul(i[0],i[1])
    time.sleep(1)




client_socket.close()
