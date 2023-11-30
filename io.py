#turn on LED
def set_led(num_pico, num_button, rgb_code):
    if num_pico == deviceID and 0 <= num_button < 16:
        keypad.illuminate(num_button, *rgb_code)
        keypad.update()

#pico Pi signal to Matrix signal
def input_interface(num_pico, num_button):
    k = num_pico // 2

    if num_pico % 2 == 1:
        row = (3 - (num_button % 4)) + (k * 4)
        col = num_button // 4
    else:
        row = (num_button % 4) + (k * 4)
        col = 3 - (num_button // 4)

    return row, col

#Matrix signal to pico Pi signal
def output_interface(row, col, rgb_code):
    if col < 4:
        num_pico = 2 * (row % 4 + 1) - 1
        num_button = 4 * (col % 4) + (3 - (row % 4))
    else:
        num_pico = 2 * (row % 4 + 1)
        num_button = 4 * (3 - (col % 4)) + (row % 4)
    
    #call set_led
    set_led(num_pico, num_button, rgb_code)
