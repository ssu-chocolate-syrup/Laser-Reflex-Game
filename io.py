from typing import Tuple
import picokeypad

keypad = picokeypad.PicoKeyPad()
keypad.set_brightness(1.0)

class IO:
    #turn on LED
    def set_led(self, device_id: int, num_pico: int, num_button: int, rgb_code: Tuple[int, int, int]) -> None:
        if num_pico == device_id and 0 <= num_button < 16:
            keypad.illuminate(num_button, *rgb_code)
            keypad.update()

    #pico Pi signal to Matrix signal
    def input_interface(self, num_pico: int, num_button: int) -> Tuple[int, int]:
        k = num_pico // 2
        if num_pico % 2 == 1:
            row = (3 - (num_button % 4)) + (k * 4)
            col = num_button // 4
        else:
            row = (num_button % 4) + (k * 4)
            col = 3 - (num_button // 4)

        return tuple(row, col)

    #Matrix signal to pico Pi signal
    def output_interface(self, row: int, col: int) -> Tuple[int, int]:
        if col < 4:
            num_pico = 2 * (row % 4 + 1) - 1
            num_button = 4 * (col // 4) + (3 - (row % 4))
        else:
            num_pico = 2 * (row % 4 + 1)
            num_button = 4 * (3 - (col // 4)) + (row % 4)
        
        return tuple(num_pico, num_button)

    def turn_on(self, row: int, col: int, rgb_code: Tuple[int, int, int]) -> None:
        num_pico, num_button = self.output_interface(row, col)
        self.set_led(num_pico, num_button, rgb_code)
        return None
