import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

digitBitmap = { 0: 0b00111111, 1: 0b00000110, 2: 0b01011011, 3: 0b01001111, 4: 0b01100110, 5: 0b01101101, 6: 0b01111101, 7: 0b00000111, 8: 0b01111111, 9: 0b01100111 }
p1_pins = {'a':17,'b':27,'c':22,'d':10,'e': 9,'f': 11,'g':0}

def p1_segment(c):
    val = digitBitmap[c]
    GPIO.output(list(p1_pins.values()), GPIO.HIGH)
    for k,v in masks.items():
        if val&v==v:
            GPIO.output(p1_pins[k], GPIO.LOW)
            
GPIO.setwarnings(False)


try:
    GPIO.setup(list(p1_pins.values()),GPIO.OUT)
    GPIO.output(list(p1_pins.values()),GPIO.LOW)
  
    p2_segment(5)

except KeyboardInterrupt:
    print("fail:(")

finally:
    time.sleep(5)
    GPIO.cleanup()