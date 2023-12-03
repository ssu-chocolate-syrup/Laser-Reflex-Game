import time
import json
import socket
import struct
from _thread import *
import network
import picokeypad

from config import Server
from config import Wifi
from config import RGB
from pico_interface import PicoInterface
from pico_io import PicoIO


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

    def _wifi_conn(self):
        try:
            self.wifi.connect(Wifi.SSID, Wifi.PW)
            while not self.wifi.isconnected():
                pass
            return True
        except:
            ErrorException('WIFI Connection Failed', self.device_id, 0).error()
            return False

    def _socket_conn(self):
        if self._wifi_conn():
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.client_socket.connect((Server.HOST, Server.PORT))
                return True
            except:
                ErrorException('Socket Connection Failed', self.device_id, 1).error()
                return False

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
            message_len = struct.unpack('!I', raw_message_len)[0]
            data = self.recv_all(client_socket, message_len).decode()
            return json.loads(data)

    def processing(self, client_socket)
        data = self.recv_data(client_socket)
        # 불 끄기
        for button in range(16):
            if self.device_id % 2 == 0 and 0 <= button < 4:
                continue
            row, col = self.pico_interface.input_interface(self.device_id, button)
            self.pico_io.run(self.device_id, row, col, self.rgb.NONE)
            time.sleep(0.03)
        # 불 켜기
        for item in data:
            row, col = self.pico_interface.input_interface(item['d'], item['b'])
            color_mapping = {
                'l': self.rgb.LASER,
                '/': self.rgb.MIRROR_LEFT2UP,
                '\\': self.rgb.MIRROR_LEFT2DOWN,
                'tn': self.rgb.TIMER,
                'tf': self.rgb.NONE,
                'p1': self.rgb.PLAYER1,
                'p2': self.rgb.PLAYER2
            }
            color = color_mapping.get(item['c'], None)
            self.pico_io.run(self.device_id, row, col, color)
            time.sleep(0.1)

    def start(self):
        if self._socket_conn():
            start_new_thread(self.processing, (self.client_socket,))
            last_button_states = 0
            print("Client Start")
            for button_id in range(16):
                row, col = self.pico_interface.input_interface(self.device_id, button_id)
                self.pico_io.run(self.device_id, row, col, self.rgb.LASER)
                time.sleep(0.1)
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
                        message = dict(d=self.device_id,
                                       b=button)
                        message_json = json.dumps(message).encode()
                        self.client_socket.sendall(struct.pack('!I', len(message_json)))
                        self.client_socket.sendall(message_json)


class ErrorException(Client):
    def __init__(self, msg, device_id, button_id):
        self.msg = msg
        self.button_id = button_id
        super().__init__(device_id)

    def error(self):
        print(self.msg)
        row, col = self.pico_interface.input_interface(self.device_id, self.button_id)
        self.pico_io.run(self.device_id, row, col, [255, 0, 0])


def main():
    app = Client(device_id=1)
    app.start()


main()
