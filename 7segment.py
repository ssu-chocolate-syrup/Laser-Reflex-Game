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


def num_out():
    try:
        GPIO.setup(list(pins.values()), GPIO.OUT)
        GPIO.output(list(pins.values()), GPIO.LOW)
        val = 0
        renderChar(p1_goalpost+1)
        renderChar(p2_goalpost+1)
    except KeyboardInterrupt:
        continue
    finally:
        GPIO.cleanup()

num_out()