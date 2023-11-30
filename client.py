import time
import json
import picokeypad
import socket
from _thread import *
import network

from wifi_config import WIFI
from server_config import Server
from interface import PicoIO

device_id = 5

keypad = picokeypad.PicoKeypad()
keypad.set_brightness(1.0)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

pico_io = PicoIO()

class CustomException:
    def __init__(self, msg, button_id):
        self.msg = msg
        self.button_id = button_id

    def error(self):
        print(self.msg)
        keypad.illuminate(self.button_id, 0x20, 0x00, 0x00)
        keypad.update()


try:
    wifi.connect(WIFI.SSID, WIFI.PW)
    while not wifi.isconnected():
        pass
except:
    CustomException('WIFI Connection Failed', 0).error()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((Server.HOST, Server.PORT))
except:
    CustomException('Socket Connection Failed', 1).error()


def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        try:
            data = json.loads(data)
            # print(data)
            print(pico_io.output_interface(data['row'], data['col']))
            if data['deviceID'] == device_id:
                pico_io.turn_on(device_id, data['row'], data['col'], [0x00, 0x20, 0x00])
                    # keypad.illuminate(int(data['buttonID']), 0x00, 0x00, 0x20)
                    # keypad.update()
        except:
            print(data)
        time.sleep(0.1)


start_new_thread(recv_data, (client_socket,))

lit = 0
last_button_states = 0
colour_index = 0

print("Client Start")

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
                        row, col = pico_io.input_interface(device_id, find)
                        message = dict(deviceID=device_id,
                                       row=row,
                                       col=col)
                        recv_json = json.dumps(message)
                        client_socket.send(recv_json.encode())
                        lit = lit | (1 << button)
                    break
                button_states >>= 1
                button += 1

