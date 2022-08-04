import RPi.GPIO as GPIO
from time import sleep


class StepperControl():

    def __init__(self, signal_pin: int, direction_pin: int, limit_switch_pin: int) -> None:
        self.signal_pin = signal_pin
        self.direction_pin = direction_pin
        self.limit_switch_pin = limit_switch_pin
        self.state = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.signal_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.limit_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.position = 0
        self.calibrate_motor()
        pass

    def calibrate_motor(self) -> None:
        # TODO: add code for calibration
        # while GPIO.input(self.limit_switch_pin):
        #     sleep(0.001)
        self.position = 0

    def setDirection(self, direction: str) -> None:
        # if direction == "forward":
        #     GPIO.output(self.direction_pin, GPIO.HIGH)
        # elif direction == "backward":
        #     GPIO.output(self.direction_pin, GPIO.LOW)

        return

    def stepForward(self) -> None:
        GPIO.output(self.direction_pin,GPIO.HIGH)
        GPIO.output(self.signal_pin,GPIO.HIGH)
        sleep(0.01)
        GPIO.output(self.signal_pin,GPIO.LOW)

    def stepBackward(self)-> None:
        GPIO.output(self.direction_pin,GPIO.LOW)
        GPIO.output(self.signal_pin,GPIO.HIGH)
        sleep(0.01)
        GPIO.output(self.signal_pin,GPIO.LOW)

    def test(self) -> int:
        if(self.state):
            # GPIO.output(self.signal_pin,GPIO.HIGH)
            # self.state = ! self.state
            pass
        else:
            # GPIO.output(self.signal_pin,GPIO.LOW)
            # self.state = ! self.state
            pass
        print(f'{self.position}')
        self.position += 1
        return self.position
