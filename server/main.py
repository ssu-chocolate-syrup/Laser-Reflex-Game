import socket
import json
import struct
from _thread import *

from game import LaserGame
from util.config import Server
from util.pico_interface import PicoInterface
from util.return_class import ReturnClass
from util.return_class import ReturnClassUtils


class LaserGameServer:
    def __init__(self):
        self.game_instance = LaserGame()
        self.pico_interface = PicoInterface()
        self.return_class_utils = ReturnClassUtils()
        self.client_sockets = []
        self.server_socket = None
        self.turn_end_button_cnt = 0

    @staticmethod
    def recv_all(client_socket, byte_size):
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
            try:
                return json.loads(data)
            except:
                return None

    def send_data_to_client(self, client, data):
        data_to_dict = [self.return_class_utils.get_convert_dict(item) for item in data]
        data_to_dict_json = json.dumps(data_to_dict).encode()
        client.sendall(struct.pack('!I', len(data_to_dict_json)))
        client.sendall(data_to_dict_json)

    def send_to_pico(self, client_socket, send_data):
        self.send_data_to_client(client_socket, send_data)
        for client in self.client_sockets:
            if client != client_socket:
                self.send_data_to_client(client, send_data)

    def win_effect(self, player):
        win_effect_send_data = []
        for col in [2, 3, 4, 7, 8, 9]:
            _device_id, _button_id = self.pico_interface.input_interface(1, col)
            win_effect_item = ReturnClass(_color_type='p1' if player == 1 else 'p2',
                                          _device_id=_device_id,
                                          _button_id=_button_id)
            win_effect_send_data.append(win_effect_item)
        for col in range(12):
            __device_id, _button_id = self.pico_interface.input_interface(2, col)
            win_effect_item = ReturnClass(_color_type='p1' if player == 1 else 'p2',
                                          _device_id=_device_id,
                                          _button_id=_button_id)
            win_effect_send_data.append(win_effect_item)
        for col in range(12):
            __device_id, _button_id = self.pico_interface.input_interface(3, col)
            win_effect_item = ReturnClass(_color_type='p1' if player == 1 else 'p2',
                                          _device_id=_device_id,
                                          _button_id=_button_id)
            win_effect_send_data.append(win_effect_item)
        for col in range(1, 11):
            __device_id, _button_id = self.pico_interface.input_interface(4, col)
            win_effect_item = ReturnClass(_color_type='p1' if player == 1 else 'p2',
                                          _device_id=_device_id,
                                          _button_id=_button_id)
            win_effect_send_data.append(win_effect_item)
        for col in range(3, 9):
            __device_id, _button_id = self.pico_interface.input_interface(5, col)
            win_effect_item = ReturnClass(_color_type='p1' if player == 1 else 'p2',
                                          _device_id=_device_id,
                                          _button_id=_button_id)
            win_effect_send_data.append(win_effect_item)
        for col in range(5, 7):
            __device_id, _button_id = self.pico_interface.input_interface(3, col)
            win_effect_item = ReturnClass(_color_type='p1' if player == 1 else 'p2',
                                          _device_id=_device_id,
                                          _button_id=_button_id)
            win_effect_send_data.append(win_effect_item)
        return win_effect_send_data

    def dfs_to_clients(self, client_socket):
        send_data = self.game_instance.main()
        self.send_to_pico(client_socket, send_data)
        self.game_instance.send_data = []

    def _click_turn_end_button(self):
        real_send_data = self.game_instance.main()
        self.turn_end_button_cnt = self.turn_end_button_cnt % 2 + 1
        _, d_id, b_id = real_send_data[-1]
        is_goal_in = self.game_instance.goal_check(d_id, b_id)
        if is_goal_in['result']:
            self.turn_end_button_cnt = 0
            real_send_data = self.win_effect(is_goal_in['player'])
            self.game_instance.init()
        else:
            real_send_data = [
                ReturnClass(_color_type=f'p{self.turn_end_button_cnt}', _device_id=4, _button_id=1),
                ReturnClass(_color_type=f'p{self.turn_end_button_cnt}', _device_id=4, _button_id=2),
                *self.game_instance.send_data
            ]
            row, col = self.pico_interface.input_interface(d_id, b_id)
            if row in [0, self.game_instance.MAX_ROW - 1]:
                real_send_data.append(ReturnClass(_color_type='tf', _device_id=d_id, _button_id=b_id))
        return real_send_data

    def threaded(self, client_socket, addr):
        print('>> Connected by:', addr[0], ':', addr[1])
        while True:
            try:
                button_input_data = self.recv_data(client_socket)
                if not button_input_data:
                    continue
                print('>> Received from', addr[0], ':', addr[1], button_input_data)
                received_data = self.return_class_utils.get_convert_return_class(button_input_data)
                row, col = self.pico_interface.input_interface(received_data.device_id, received_data.button_id)
                if row in (5, 6) and col == 7:
                    real_send_data = self._click_turn_end_button()
                    self.send_to_pico(client_socket, real_send_data)
                    self.game_instance.send_data = []
                elif col != 7:
                    self.game_instance.input_mirror(row, col)
                    self.dfs_to_clients(client_socket)
            except ConnectionResetError as e:
                print('>> Disconnected by', addr[0], ':', addr[1])
                break

        if client_socket in self.client_sockets:
            self.client_sockets.remove(client_socket)
            print('remove client list:', len(self.client_sockets))
        client_socket.close()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1 << 13)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32)
        self.server_socket.bind(('0.0.0.0', Server.PORT))
        self.server_socket.listen()
        print('>> Server Start with ip:', Server.HOST)

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
