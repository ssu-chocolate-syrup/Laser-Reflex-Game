import RPi.GPIO as GPIO
import time

buzzer = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setwarnings(False)

pwm = GPIO(buzzer, 262)

pwm.start(50.0)
time.sleep(1)

pwm.stop()
GPIO.cleanup()