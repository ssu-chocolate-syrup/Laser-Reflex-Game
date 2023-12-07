import time
import json
import socket
import struct
from _thread import *
import network
import picokeypad

from util.config import Server
from util.config import Wifi
from util.config import RGB
from util.pico_interface import PicoInterface
from util.pico_io import PicoIO
from util.return_class import ReturnClass
from util.return_class import ReturnClassUtils


def power_of_2(number):
    count = 0
    while number > 0:
        number >>= 1
        count += 1
    return count - 1


class Client:
    def __init__(self, device_id):
        self.device_id = device_id
        self.keypad = picokeypad.PicoKeypad()
        self.keypad.set_brightness(0)
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)
        self.client_socket = None
        self.pico_io = PicoIO()
        self.pico_interface = PicoInterface()
        self.rgb = RGB()
        self.return_class_utils = ReturnClassUtils()
        self.color_mapping = {
            'l': self.rgb.LASER,
            '/': self.rgb.MIRROR_LEFT2UP,
            '\\': self.rgb.MIRROR_LEFT2DOWN,
            'tn': self.rgb.TIMER,
            'tf': self.rgb.NONE,
            'p1': self.rgb.PLAYER1,
            'p2': self.rgb.PLAYER2
        }

    def _wifi_conn(self):
        try:
            self.wifi.connect(Wifi.SSID, Wifi.PW)
            while not self.wifi.isconnected():
                pass
            print('WIFI is Connected')
            return True
        except:
            ErrorException('WIFI Connection Failed', self.device_id, 0).error()
            return False

    def _socket_conn(self):
        if self._wifi_conn():
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.client_socket.connect((Server.HOST, Server.PORT))
                print('Socket is Connected')
                return True
            except:
                ErrorException('Socket Connection Failed', self.device_id, 1).error()
                return False

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
                data_json = json.loads(data)
                data = [self.return_class_utils.get_convert_return_class(item) for item in data_json]
                return data
            except:
                return None

    def processing(self, client_socket):
        while True:
            data = self.recv_data(client_socket)
            # 불 끄기
            for button in range(16):
                '''if self.device_id % 2 == 0 and 0 <= button < 4:
                    continue'''
                row, col = self.pico_interface.input_interface(self.device_id, button)
                self.pico_io.run(self.device_id, row, col, self.rgb.NONE)

            # 불 켜기
            if not data:
                break
            for item in data:
                _color_type, _device_id, _button_id = item
                row, col = self.pico_interface.input_interface(_device_id, _button_id)
                self.pico_io.run(self.device_id, row, col, self.color_mapping.get(_color_type, None))
                time.sleep(0.05)

    def start(self):
        if not self._socket_conn():
            return

        start_new_thread(self.processing, (self.client_socket,))
        last_button_states = 0
        print("Client Start")
        for button_id in range(16):
            row, col = self.pico_interface.input_interface(self.device_id, button_id)
            self.pico_io.run(self.device_id, row, col, self.rgb.LASER)
            time.sleep(0.5)
        for button_id in range(16):
            row, col = self.pico_interface.input_interface(self.device_id, button_id)
            self.pico_io.run(self.device_id, row, col, self.rgb.NONE)

        while True:
            button_states = self.keypad.get_button_states()
            if last_button_states != button_states:
                last_button_states = button_states
                if button_states > 0:
                    button = power_of_2(button_states)
                    row, col = self.pico_interface.input_interface(self.device_id, button)
                    if row in [0, 11]:
                        continue
                    send_data = ReturnClass(_color_type=None, _device_id=self.device_id, _button_id=button)
                    send_data_json = self.return_class_utils.get_convert_json(send_data)
                    send_data_json_encode = send_data_json.encode()
                    self.client_socket.sendall(struct.pack('!I', len(send_data_json_encode)))
                    self.client_socket.sendall(send_data_json_encode)


class ErrorException(Client):
    def __init__(self, msg, device_id, button_id):
        self.msg = msg
        self.button_id = button_id
        super().__init__(device_id)

    def error(self):
        print(self.msg)
        row, col = self.pico_interface.input_interface(self.device_id, self.button_id)
        self.pico_io.run(self.device_id, row, col, self.rgb.RED)


def main():
    app = Client(device_id=1)
    app.start()


main()
