class PicoIO:
    # turn on LED
    def set_led(self, num_pico, num_button, check_num_pico, rgb_code):
        if num_pico == check_num_pico and 0 <= num_button < 16:
            import picokeypad

            keypad = picokeypad.PicoKeyPad()
            keypad.set_brightness(1.0)

            keypad.illuminate(num_button, *rgb_code)
            keypad.update()

    # pico Pi signal to Matrix signal
    def input_interface(self, num_pico, num_button):
        k = num_pico // 2
        if num_pico % 2 == 1:
            row = (3 - (num_button % 4)) + (k * 4)
            col = num_button // 4
        else:
            row = (num_button % 4) + ((k - 1) * 4)
            col = 3 - (num_button // 4) + 4

        return row, col

    # Matrix signal to pico Pi signal
    def output_interface(self, row, col):
        if col < 4:
            num_pico = 2 * (row % 4 + 1) - 1
            num_button = 4 * (col // 4) + (3 - (row % 4))
        else:
            num_pico = 2 * (row % 4 + 1)
            num_button = 4 * (3 - (col // 4)) + (row % 4)

        return num_pico, num_button

    def turn_on(self, check_num_pico, row, col, rgb_code):
        num_pico, num_button = self.output_interface(row, col)
        self.set_led(num_pico, num_button, check_num_pico, rgb_code)
        return None

