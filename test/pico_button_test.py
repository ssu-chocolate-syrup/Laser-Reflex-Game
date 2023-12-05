"""
Test Title: Click Pico Button -> Turn On LED
"""

import picokeypad

from util.config import RGB
from util.pico_interface import PicoInterface
from util.pico_io import PicoIO


class PicoButtonTest:
    def __init__(self, device_id):
        self.device_id = device_id
        self.keypad = picokeypad.PicoKeypad()
        self.keypad.set_brightness(0)
        self.pico_io = PicoIO()
        self.pico_interface = PicoInterface()
        self.rgb = RGB()
        self.last_button_states = 0

    @staticmethod
    def _power_of_2(number):
        count = 0
        while number > 0:
            number >>= 1
            count += 1
        return count - 1

    def run(self):
        print("< Test Start >")
        while True:
            button_states = self.keypad.get_button_states()
            if self.last_button_states != button_states:
                self.last_button_states = button_states
                if button_states > 0:
                    button = self._power_of_2(button_states)
                    row, col = self.pico_interface.input_interface(self.device_id, button)
                    print(f"buttonID: {button} | row: {row} | col: {col}")
                    self.pico_io.run(self.device_id, row, col, self.rgb.BLUE)


if __name__ == '__main__':
    test = PicoButtonTest(device_id=1)
    test.run()