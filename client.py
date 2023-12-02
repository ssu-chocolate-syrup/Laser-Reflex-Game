import time
import json
import picokeypad
import socket
import struct
from _thread import *
import network

from config import Server
from config import Wifi
from config import RGB
from pico_interface import PicoInterface
from pico_io import PicoIO

device_id = 1

keypad = picokeypad.PicoKeypad()
keypad.set_brightness(0)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

pico_io = PicoIO()
pico_interface = PicoInterface()


def power_of_2(number):
    count = 0
    while number > 0:
        number >>= 1
        count += 1
    return count - 1


class ErrorException:
    def __init__(self, msg, button_id):
        self.msg = msg
        self.button_id = button_id

    def error(self):
        print(self.msg)
        row, col = pico_interface.input_interface(device_id, self.button_id)
        pico_io.run(device_id, row, col, [255, 0, 0])


try:
    wifi.connect(Wifi.SSID, Wifi.PW)
    while not wifi.isconnected():
        pass
except:
    ErrorException('WIFI Connection Failed', 0).error()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((Server.HOST, Server.PORT))
except:
    ErrorException('Socket Connection Failed', 1).error()


def recv_all(client_socket, n):
    data = b''
    while len(data) < n:
        packet = client_socket.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


def recv_data(client_socket):
    while True:
        raw_msglen = recv_all(client_socket, 4)
        msglen = struct.unpack('!I', raw_msglen)[0]
        data = recv_all(client_socket, msglen).decode()
        data = json.loads(data)
        for button in range(16):
            row, col = pico_interface.input_interface(device_id, button)
            pico_io.run(device_id, row, col, RGB.NONE)
        for item in data:
            row, col = pico_interface.input_interface(item['d'], item['b'])
            color = None
            if item['c'] == '/':
                color = RGB.MIRROR_LEFT2UP
            elif item['c'] == '\\':
                color = RGB.MIRROR_LEFT2DOWN
            elif item['c'] == 'l':
                color = RGB.LASER
            pico_io.run(device_id, row, col, item['c'])
            time.sleep(0.05)


start_new_thread(recv_data, (client_socket,))
last_button_states = 0

print("Client Start")
for button_id in range(16):
    row, col = pico_interface.input_interface(device_id, button_id)
    pico_io.run(device_id, row, col, RGB.LASER)
    time.sleep(0.1)

for button_id in range(16):
    row, col = pico_interface.input_interface(device_id, button_id)
    pico_io.run(device_id, row, col, RGB.NONE)

while True:
    button_states = keypad.get_button_states()
    if last_button_states != button_states:
        last_button_states = button_states
        if button_states > 0:
            button = power_of_2(button_states)
            message = dict(d=device_id,
                           b=button)
            message_json = json.dumps(message)
            client_socket.sendall(message_json.encode())
