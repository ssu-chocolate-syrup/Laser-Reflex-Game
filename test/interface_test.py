"""
Test Title: Turn on all picopad LED
"""

import time

from config import RGB
from pico_interface import PicoInterface
from pico_io import PicoIO


class PicoInterfaceTest:
    def __init__(self):
        self.pico_io = PicoIO()
        self.pico_interface = PicoInterface()
        self.rgb = RGB()

    def run(self):
        print("< Test Start >")
        for device_id in range(1, 6 + 1):
            for button_id in range(16):
                row, col = self.pico_interface.input_interface(device_id, button_id)
                print(f"{device_id}: {self.pico_interface.output_interface(row, col)}")
                self.pico_io.run(device_id, row, col, self.rgb.GREEN)
                time.sleep(0.1)
            time.sleep(1)


if __name__ == '__main__':
    test = PicoInterfaceTest()
    test.run()
