import time
import json
import picokeypad
import socket
from _thread import *
import network

from config import Server
from config import Wifi
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


def recv_data(client_socket):
    while True:
        data = None
        try:
            data = client_socket.recv(1024 * 10).decode()
            data = json.loads(data)
            for button in range(16):
                row, col = pico_interface.input_interface(device_id, button)
                pico_io.run(device_id, row, col, (0, 0, 0))
            for item in data:
                row, col = pico_interface.input_interface(item['deviceID'], item['buttonID'])
                pico_io.run(device_id, row, col, item['rgb'])
                time.sleep(0.1)
        except:
            print(data)
            # pico_io.run(device_id)


start_new_thread(recv_data, (client_socket,))
last_button_states = 0

print("Client Start")
for button_id in range(16):
    row, col = pico_interface.input_interface(device_id, button_id)
    pico_io.run(device_id, row, col, (250, 146, 0))
    time.sleep(0.1)

for button_id in range(16):
    row, col = pico_interface.input_interface(device_id, button_id)
    pico_io.run(device_id, row, col, (0, 0, 0))

while True:
    button_states = keypad.get_button_states()
    if last_button_states != button_states:
        last_button_states = button_states
        if button_states > 0:
            button = power_of_2(button_states)
            message = dict(deviceID=device_id,
                           buttonID=button)
            message_json = json.dumps(message)
            client_socket.send(message_json.encode())
