import time

from pico_interface import PicoInterface
from pico_io import PicoIO

io = PicoIO()
interface = PicoInterface()

for device_id in range(1, 6 + 1):
    for button_id in range(16):
        row, col = interface.input_interface(device_id, button_id)
        print(f"{device_id}: {interface.output_interface(row, col)}")
        io.run(device_id, row, col, (255, 0, 0))
        time.sleep(1)
    time.sleep(3)
