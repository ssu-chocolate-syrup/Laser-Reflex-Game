class PicoInterface:
    # pico Pi signal to Matrix signal
    @staticmethod
    def input_interface(num_pico, num_button):
        if not isinstance(num_pico, int) or not isinstance(num_button, int):
            num_pico, num_button = map(int, [num_pico, num_button])
        k = num_pico // 2
        if num_pico % 2 == 1:
            row = (3 - (num_button % 4)) + (k * 4)
            col = num_button // 4
        else:
            row = (num_button % 4) + ((k - 1) * 4)
            col = 3 - (num_button // 4) + 4

        return row, col

    # Matrix signal to pico Pi signal
    @staticmethod
    def output_interface(row, col):
        if not isinstance(row, int) or not isinstance(col, int):
            row, col = map(int, [row, col])
        if col < 4:
            num_pico = 2 * (row // 4 + 1) - 1
            num_button = 4 * col + (3 - (row % 4))
        else:
            num_pico = 2 * (row // 4 + 1)
            num_button = 4 * (3 - (col - 4)) + (row % 4)

        return num_pico, num_button
