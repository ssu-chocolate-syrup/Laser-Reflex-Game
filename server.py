import socket
import json
import time
import threading
import struct
from _thread import *

from game import LaserGame
from config import Server
from pico_interface import PicoInterface


class LaserGameServer:
    def __init__(self):
        self.game_instance = LaserGame()
        self.pico_interface = PicoInterface()
        self.client_sockets = []
        self.server_socket = None

    def recv_all(self, client_socket, byte_size):
        data = b''
        while len(data) < byte_size:
            packet = client_socket.recv(byte_size - len(data))
            if not packet:
                return None
            data += packet
        return data

    def recv_data(self, client_socket):
        while True:
            raw_msglen = self.recv_all(client_socket, 4)
            msglen = struct.unpack('!I', raw_msglen)[0]
            data = self.recv_all(client_socket, msglen).decode()
            data = json.loads(data)
            return data

    # def timer_thread_function(self, count):
    #     time.sleep(3)
    #     p1_pico_number_id, p1_pico_number_button = self.pico_interface.output_interface(12 - 1 - count, 8 - 1)
    #     p2_pico_number_id, p2_pico_number_button = self.pico_interface.output_interface(count, 8 - 1)

    #     send_data = [dict(c='tf', d=p1_pico_number_id, b=p1_pico_number_button),
    #                  dict(c='tf', d=p2_pico_number_id, b=p2_pico_number_button)]
    #     send_data_json = json.dumps(send_data).encode()
    #     # print(send_data_json)
    #     for client in self.client_sockets:
    #         client.sendall(struct.pack('!I', len(send_data_json)))
    #         client.sendall(send_data_json)

    # def timer_thread(self, is_init, count):
    #     if not is_init:
    #         send_data = []
    #         for p2_row in range(11, 7 - 1, -1):
    #             p1_row = p2_row - 7
    #             p1_pico_number_id, p1_pico_number_button = self.pico_interface.output_interface(p1_row, 8 - 1)
    #             p2_pico_number_id, p2_pico_number_button = self.pico_interface.output_interface(p2_row, 8 - 1)
    #             send_data.append(dict(c='tn', d=p1_pico_number_id, b=p1_pico_number_button))
    #             send_data.append(dict(c='tn', d=p2_pico_number_id, b=p2_pico_number_button))
    #         send_data_json = json.dumps(send_data).encode()
    #         print(send_data_json)
    #         for client in self.client_sockets:
    #             client.sendall(struct.pack('!I', len(send_data_json)))
    #             client.sendall(send_data_json)
    #         self.timer_thread_function(count)
    #         threading.Thread(target=self.timer_thread, args=(1, count - 1)).start()
    #     else:
    #         if count > 0:
    #             self.timer_thread_function(count)
    #             threading.Thread(target=self.timer_thread, args=(1, count - 1)).start()
    #         elif count == 0:
    #             self.timer_thread_function(count)
    #             threading.Thread(target=self.timer_thread, args=(0, count + 4)).start()
    
    #반복되는 전송 처리해주기위해 함수 처리
    def send_to_pico(clinet_socket,send_data):
        print(send_data)
        ## 실제 전송
        client_socket.sendall(struct.pack('!I', len(send_data)))
        client_socket.sendall(send_data)
        for client in self.client_sockets:
            if client != client_socket:
                client.sendall(struct.pack('!I', len(send_data)))
                client.sendall(send_data)
    
    #승리 이펙트 계산함수 (effect_type이 모든 피코파이의 button_num=0에 도달하면, 각 client에서 이펙트 실행)
    def win_effect(player):
        send_data = []
        if (player == 1):
            effect_type ='' ##effect type 추가해주세요, player1
        elif (player == 2):
            effect_type ='' ##effect type 추가해주세요, player2
        for i in range(6):
            send_data.append(dict(
                c= effect_type, 
                d= i,
                b= 0
            ))
        return send_data
    #승리 이펙트 전송함수
    def effect_to_clients(client_socket):
        check=self.game_instance.goal_check()
        if (check==1): ##p1이 승리
            send_data = json.dumps(win_effect(1))
            send_to_pico(client_socket,send_data)
            time(1)
            #이펙트 출력 완료까지 대기
            time.sleep(1)

        elif (check==2): ##p2가 승리
            send_data = json.dumps(win_effect(2))
            send_to_pico(client_socket,send_data)
            #이펙트 출력 완료까지 대기
            time.sleep(1)

    #dfs 전송 함수
    def dfs_to_clients(client_socket,row,col):
        self.game_instance.input_mirror(row, col)
        send_data = json.dumps(self.game_instance.main()).encode()
        send_to_pico(client_socket,send_data)

    def threaded(self, client_socket, addr):
        print('>> Connected by :', addr[0], ':', addr[1])

        while True:
            try:
                data = self.recv_data(client_socket)
                print('>> Received from ' + addr[0], ':', addr[1], data)
                row, col = self.pico_interface.input_interface(data['d'], data['b'])
                #턴버튼 7,5 or 7,6으로 추가 effect_send함수 추가
                if (row == 7 and col == 5)or(row == 7 and col == 6):
                    # threading.Thread(target=self.timer_thread, args=(0, 4)).start()
                    #이펙트 전송 함수
                    effect_to_clients(client_socket)
                    #dfs 전송 함수
                    dfs_to_clients(client_socket,row,col)

                else:
                    #dfs 전송함수
                    dfs_to_clients(client_socket,row,col)
            except ConnectionResetError as e:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break

        if client_socket in self.client_sockets:
            self.client_sockets.remove(client_socket)
            print('remove client list : ', len(self.client_sockets))

        client_socket.close()

    def start_server(self):
        print('>> Server Start with ip :', Server.HOST)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1 << 13)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32)
        self.server_socket.bind(('0.0.0.0', Server.PORT))
        self.server_socket.listen()

        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                self.client_sockets.append(client_socket)
                start_new_thread(self.threaded, (client_socket, addr))
                print("참가자 수 : ", len(self.client_sockets))
        except Exception as e:
            print('에러 : ', e)
        finally:
            self.server_socket.close()


if __name__ == "__main__":
    game_server = LaserGameServer()
    game_server.start_server()
