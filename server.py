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
        self.turn_end_button_cnt = 0
        self.current_timer_thread = None
        self.timer_stop_flag = False  # 타이머 중지 플래그 추가
        self.timer_completed = threading.Event()  # 타이머 완료 이벤트
        self.timer_reset_flag = threading.Event()  # 타이머 리셋 플래그 추가

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
            raw_message_len = self.recv_all(client_socket, 4)
            if not raw_message_len:
                return None
            message_len = struct.unpack('!I', raw_message_len)[0]
            data = self.recv_all(client_socket, message_len).decode()
            data = json.loads(data)
            return data

    ##타이머 초 세주는 함수
    def timer_thread_function(self, count):
        initial_count = count  # 초기 count 값 저장
        while True:
            while count >= 0:
                # 중지 신호가 있으면 타이머 스레드 종료
                if self.timer_reset_flag.is_set():
                    return
                send_data = []
                ##타이머 줄어들때마다 타이머 종료 신호 뿌려줌
                for player_row in [self.game_instance.MAX_ROW - 1 - count, count]:
                    pico_number_id, pico_number_button = self.pico_interface.output_interface(player_row,
                                                                                              self.game_instance.MAX_COL)
                    send_data.append([dict(c='tf', d=pico_number_id, b=pico_number_button)])
                send_data_json = json.dumps(send_data).encode()
                print(send_data_json)
                for client in self.client_sockets:
                    self.send_data_to_client(client, send_data_json)
                time.sleep(1)
                count -= 1
            # 타이머 완료 플래그 설정
            self.timer_completed.set()
            # 다시 처음부터 count
            count = initial_count

    ##타이머 제시작 함수
    def check_and_restart_timer(self):
        if self.timer_completed.is_set():
            self.timer_completed.clear()  # 플래그 초기화
            self.start_timer_thread(5)  # 타이머 재시작

    ##타이머 시작 함수
    def start_timer_thread(self, count):
        # 현재 실행 중인 타이머 스레드가 있으면 중지 신호를 보내고 기다림
        self.timer_reset_flag.set()  # 타이머 중지 신호
        if self.current_timer_thread and self.current_timer_thread.is_alive():
            self.current_timer_thread.join()  # 기존 타이머 종료 대기

        self.timer_reset_flag.clear()  # 중지 신호 초기화
        self.timer_completed.clear()  # 타이머 완료 플래그 초기화

        # 타이머 LED 모든 피코패드에 뿌려줌
        send_data = []
        for p2_row in range(self.game_instance.MAX_ROW - 1, self.game_instance.MAX_COL - 1, -1):
            p1_row = p2_row - 7
            for player_row in [p1_row, p2_row]:
                pico_number_id, pico_number_button = self.pico_interface.output_interface(player_row,
                                                                                          self.game_instance.MAX_COL)
                send_data.extend([dict(c='tn', d=pico_number_id, b=pico_number_button)])
        send_data_json = json.dumps(send_data).encode()
        print(send_data_json)
        for client in self.client_sockets:
            self.send_data_to_client(client, send_data_json)

        ##타이머 count 시작
        self.current_timer_thread = threading.Thread(target=self.timer_thread_function, args=(count,))
        self.current_timer_thread.start()

    @staticmethod
    def send_data_to_client(client, data):
        client.sendall(struct.pack('!I', len(data)))
        client.sendall(data)

    def send_to_pico(self, client_socket, send_data):
        print(send_data)
        self.send_data_to_client(client_socket, send_data)
        for client in self.client_sockets:
            if client != client_socket:
                self.send_data_to_client(client, send_data)

    def win_effect(self, player):
        return [dict(c='p1' if player == 1 else 'p2',
                     d=device_id,
                     b=15)
                for device_id in range(1, 6 + 1)]

    def dfs_to_clients(self, client_socket):
        self.game_instance.main()
        send_data = json.dumps(self.game_instance.send_data).encode()
        self.send_to_pico(client_socket, send_data)

    def threaded(self, client_socket, addr):
        print('>> Connected by:', addr[0], ':', addr[1])
        while True:
            try:
                button_input_data = self.recv_data(client_socket)
                if not button_input_data:
                    continue
                print(button_input_data)
                print('>> Received from', addr[0], ':', addr[1], button_input_data)
                row, col = self.pico_interface.input_interface(button_input_data['d'], button_input_data['b'])
                if (row == 5 and col == 7) or (row == 6 and col == 7):
                    print('hi')
                    ##타이머 시작 부분, 주석처리 함
                    ##self.start_timer_thread(5) 
                    if self.turn_end_button_cnt == 0:
                        self.dfs_to_clients(client_socket)
                        self.turn_end_button_cnt += 1
                    elif self.turn_end_button_cnt == 1:
                        self.turn_end_button_cnt += 1
                    elif self.turn_end_button_cnt == 2:
                        self.turn_end_button_cnt -= 1
                    goal_check = self.game_instance.goal_check()
                    if goal_check['result']:
                        self.turn_end_button_cnt = 0
                        send_data = json.dumps(self.win_effect(goal_check['player']))
                        self.game_instance.init()
                    else:
                        send_data = [dict(c=f'p{self.turn_end_button_cnt}',
                                          d=button_input_data['d'],
                                          b=button_input_data['b'])]
                        for item in self.game_instance.send_data:
                            send_data.append(item)
                        send_data = json.dumps(send_data).encode()
                        print(send_data)

                    self.send_to_pico(client_socket, send_data.encode())
                    ## 5,7입력들어오면 현재 실행중인 타이머 종료, 타이머 재시작
                    ##self.check_and_restart_timer() 

                else:
                    self.game_instance.input_mirror(row, col)
                    print(row, col)
                    self.dfs_to_clients(client_socket)

            except ConnectionResetError as e:
                print('>> Disconnected by', addr[0], ':', addr[1])
                break

        if client_socket in self.client_sockets:
            self.client_sockets.remove(client_socket)
            print('remove client list:', len(self.client_sockets))

        client_socket.close()

    def start_server(self):
        print('>> Server Start with ip:', Server.HOST)
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
                print("참가자 수:", len(self.client_sockets))
        except Exception as e:
            print('에러:', e)
        finally:
            self.server_socket.close()


if __name__ == "__main__":
    game_server = LaserGameServer()
    game_server.start_server()
