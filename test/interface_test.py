from interface import PicoIO
import time

io = PicoIO()

for device_id in range(1, 6 + 1):
    for button_id in range(16):
        row, col = io.input_interface(device_id, button_id)
        print(f"{device_id}: {io.output_interface(row, col)}")
        io.turn_on(device_id, row, col, (255, 0, 0))
        time.sleep(1)
    time.sleep(3)
