import RPi.GPIO as GPIO
from time import sleep


class ConveyerControl():
    def __init__(self, pin: int, delay_time: float) -> None:
        self.pin = pin
        self.delay_time = delay_time
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)

    def load(self) -> None:
        GPIO.output(self.pin, GPIO.HIGH)
        sleep(self.delay_time)
        GPIO.output(self.pin, GPIO.LOW)
