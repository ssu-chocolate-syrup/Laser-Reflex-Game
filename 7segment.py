import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

digitBitmap = {1: 0b00000110,2:0b01011011,3:0b01001111,5:0b01101101,6: 0b01111101,7:0b00000111}
masks = {'a':0b00000001,'b':0b00000010,'c':0b00000100, 'd':0b00001000,'e':0b00010000, 'f':0b00100000,'g':0b01000000}
p1_pins = {'a':17,'b':27,'c':22,'d':10,'e': 9,'f': 11,'g':0}
p2_pins = {'a':23,'b':24,'c':25,'d':8,'e':7,'f':1,'g':12}

def p1_segment(c):
    val = digitBitmap[c]
    GPIO.output(list(p1_pins.values()), GPIO.LOW)
    for k,v in masks.items():
        if val&v==v:
            GPIO.output(p1_pins[k], GPIO.HIGH)

def p2_segment(c):
    val = digitBitmap[c]
    GPIO.output(list(p2_pins.values()), GPIO.LOW)
    for k,v in masks.items():
        if val&v==v:
            GPIO.output(p2_pins[k], GPIO.HIGH)

GPIO.setwarnings(False)

GPIO.setup(list(p1_pins.values()),GPIO.OUT)
GPIO.output(list(p1_pins.values()),GPIO.LOW)

GPIO.setup(list(p2_pins.values()), GPIO.OUT)
GPIO.output(list(p2_pins.values()), GPIO.LOW)

p1_segment(1)
time.sleep(10)

GPIO.cleanup()
