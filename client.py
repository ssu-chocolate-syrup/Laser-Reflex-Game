import time
import json
import picokeypad
from machine import UART, Pin
import socket
from _thread import *
import network

from wifi_config import WIFI

# PicoPad Device ID (Manual, 1~6)
deviceID = 2

keypad = picokeypad.PicoKeypad()
keypad.set_brightness(1.0)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI.SSID, WIFI.PW)

while not wifi.isconnected():
    pass

HOST = '192.168.207.199'
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def recv_data(client_socket):
    while True:
        data = client_socket.recv(32).decode()
        try:
            data = json.loads(data)
            # Except Same Device ID
            # if deviceID in data['cmdDeviceID']: -> Time Complexity : O(log N)

            if data['deviceID'] != deviceID:
                # Picokey().illuminate(buttonId: int, Red: int, Green: int, Blue: int)
                keypad.illuminate(int(data['buttonID']), 0x00, 0x00, 0x20)
            # Update -> Save RGB code
            keypad.update()
        except:
            print(data)


start_new_thread(recv_data, (client_socket,))

lit = 0
last_button_states = 0
colour_index = 0

NUM_PADS = keypad.get_num_pads()
while True:
    button_states = keypad.get_button_states()
    if last_button_states != button_states:
        last_button_states = button_states
        if button_states > 0:
            # if lit == 0xffff:
            #     lit = 0
            #     colour_index += 1
            #     if colour_index >= 6:
            #         colour_index = 0
            # else:
            button = 0
            for find in range(0, NUM_PADS):
                if button_states & 0x01 > 0:
                    if not (button_states & (~0x01)) > 0:
                        # JSON Data Type Casting
                        message: dict = {'deviceID': deviceID, 'buttonID': find, 'cmdDeviceID': [1, 2, 3, 4]}
                        recv_json = json.dumps(message)
                        # JSON Data Send to Server
                        client_socket.send(recv_json.encode())
                        lit = lit | (1 << button)
                    break
                button_states >>= 1
                button += 1

'''
    for i in range(0, NUM_PADS):
        if (lit >> i) & 0x01:
            if colour_index == 0:
                keypad.illuminate(i, 0x00, 0x20, 0x00)
            elif colour_index == 1:
                keypad.illuminate(i, 0x20, 0x20, 0x00)
            elif colour_index == 2:
                keypad.illuminate(i, 0x20, 0x00, 0x00)
            elif colour_index == 3:
                keypad.illuminate(i, 0x20, 0x00, 0x20)
            elif colour_index == 4:
                keypad.illuminate(i, 0x00, 0x00, 0x20)
            elif colour_index == 5:
                keypad.illuminate(i, 0x00, 0x20, 0x20)
        else:
            keypad.illuminate(i, 0x05, 0x05, 0x05)

    keypad.update()

    time.sleep(0.1)
'''
