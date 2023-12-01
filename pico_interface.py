class PicoInterface:
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
            num_pico = 2 * (row // 4 + 1) - 1
            num_button = 4 * col + (3 - (row % 4))
        else:
            num_pico = 2 * (row // 4 + 1)
            num_button = 4 * (3 - (col - 4)) + (row % 4)

        return num_pico, num_button