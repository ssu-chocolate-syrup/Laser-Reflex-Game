import time
import RPi.GPIO as GPIO

class SevenSegmentDisplay:
    def __init__(self, p1_pins, p2_pins, digitBitmap, masks):
        self.p1_pins = p1_pins
        self.p2_pins = p2_pins
        self.digitBitmap = digitBitmap
        self.masks = masks

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(list(self.p1_pins.values()), GPIO.OUT)
        GPIO.output(list(self.p1_pins.values()), GPIO.LOW)

        GPIO.setup(list(self.p2_pins.values()), GPIO.OUT)
        GPIO.output(list(self.p2_pins.values()), GPIO.LOW)

    def p1_segment(self, c):
        val = self.digitBitmap[c]
        GPIO.output(list(self.p1_pins.values()), GPIO.HIGH)
        for k, v in self.masks.items():
            if val & v == v:
                GPIO.output(self.p1_pins[k], GPIO.LOW)

    def p2_segment(self, c):
        val = self.digitBitmap[c]
        GPIO.output(list(self.p2_pins.values()), GPIO.HIGH)
        for k, v in self.masks.items():
            if val & v == v:
                GPIO.output(self.p2_pins[k], GPIO.LOW)

    def display_numbers(self, p1_digit, p2_digit):
        self.p1_segment(p1_digit)
        self.p2_segment(p2_digit)

    def cleanup(self):
        GPIO.cleanup()

# Example usage
if __name__ == "__main__":
    digitBitmap = {1: 0b00000110, 2: 0b01011011, 3: 0b01001111, 5: 0b01101101, 6: 0b01111101, 7: 0b00000111}
    masks = {'a': 0b00000001, 'b': 0b00000010, 'c': 0b00000100, 'd': 0b00001000, 'e': 0b00010000, 'f': 0b00100000, 'g': 0b01000000}
    p1_pins = {'a': 17, 'b': 27, 'c': 22, 'd': 10, 'e': 9, 'f': 11, 'g': 0}
    p2_pins = {'a': 23, 'b': 24, 'c': 25, 'd': 8, 'e': 7, 'f': 1, 'g': 12}
    
    display = SevenSegmentDisplay(p1_pins, p2_pins, digitBitmap, masks)