import picokeypad
from pico_interface import PicoInterface

keypad = picokeypad.PicoKeypad()
keypad.set_brightness(1.0)

interface = PicoInterface()


class PicoIO:
    # turn on LED
    @staticmethod
    def set_led(num_pico, num_button, check_num_pico, rgb_code):
        if num_pico == check_num_pico and 0 <= num_button < 16:
            keypad.illuminate(num_button, *rgb_code)
            keypad.update()
            return True
        return False

    def run(self, check_num_pico, row, col, rgb_code):
        num_pico, num_button = interface.output_interface(row, col)
        self.set_led(num_pico, num_button, check_num_pico, rgb_code)
        return None
