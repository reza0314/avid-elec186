import RPi.GPIO as GPIO
from time import sleep


class ConveyerControl():
    def __init__(self, pin: int, delay_time: int) -> None:
        self.pin = pin
        self.delay_time = delay_time
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUTPUT)
        
        pass

    def load(self):
        GPIO.output(self.pin, GPIO.HIGH)
        sleep(self.delay_time)
        GPIO.output(self.pin, GPIO.LOW)
