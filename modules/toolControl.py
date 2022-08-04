import RPi as GPIO


class ToolControl():
    def __init__(self, pin: int) -> None:
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUTPUT)
        pass

    def pick(self):
        GPIO.output(self.pin,GPIO.HIGH)
    def place(self):
        GPIO.output(self.pin,GPIO.LOW)
