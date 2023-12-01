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

device_id = 3

keypad = picokeypad.PicoKeypad()
keypad.set_brightness(0)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

pico_io = PicoIO()
pico_interface = PicoInterface()


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
        try:
            data = client_socket.recv(100).decode()
            data = json.loads(data)
            print(data)
            if data['deviceID'] == device_id:
                pico_io.run(device_id, data['row'], data['col'], [0, 255, 0])
        except:
            print(type(data))


start_new_thread(recv_data, (client_socket,))

lit = 0
last_button_states = 0
colour_index = 0

print("Client Start")
for button_id in range(16):
    row, col = pico_interface.input_interface(device_id, button_id)
    pico_io.run(device_id, row, col, (250, 146, 0))
    time.sleep(0.1)

for button_id in range(16):
    row, col = pico_interface.input_interface(device_id, button_id)
    pico_io.run(device_id, row, col, (0, 0, 0))

NUM_PADS = keypad.get_num_pads()
while True:
    button_states = keypad.get_button_states()
    if last_button_states != button_states:
        last_button_states = button_states
        if button_states > 0:
            button = 0
            for find in range(0, NUM_PADS):
                if button_states & 0x01 > 0:
                    if not (button_states & (~0x01)) > 0:
                        row, col = pico_interface.input_interface(device_id, find)
                        message = dict(deviceID=device_id,
                                       row=row,
                                       col=col)
                        recv_json = json.dumps(message)
                        client_socket.send(recv_json.encode())
                        lit = lit | (1 << button)
                    break
                button_states >>= 1
                button += 1
