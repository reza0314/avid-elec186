import RPi.GPIO as GPIO
from time import sleep


class StepperControl():

    def __init__(self, signal_pin: int, direction_pin: int, limit_switch_pin: int, limit_direction: str) -> None:
        self.signal_pin = signal_pin
        self.direction_pin = direction_pin
        self.limit_switch_pin = limit_switch_pin
        self.state = True
        self.limit_direction = limit_direction
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.signal_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.limit_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.position = 0
        self.calibrate_motor()

    def calibrate_motor(self) -> None:
        if self.limit_direction == "backward":
            while GPIO.input(self.limit_switch_pin):
                self.stepBackward()
        elif self.limit_direction == "forward":
            while GPIO.input(self.limit_switch_pin):
                self.stepForward()
        else :
            print("There was a problem with initilization")
            exit()
        self.position = 0
        print("calibration done")

    def stepForward(self) -> int:
        GPIO.output(self.direction_pin, GPIO.HIGH)
        GPIO.output(self.signal_pin, GPIO.HIGH)
        sleep(0.01)
        GPIO.output(self.signal_pin, GPIO.LOW)
        sleep(0.01)
        self.position += 1
        return self.position

    def stepBackward(self) -> int:
        GPIO.output(self.direction_pin, GPIO.LOW)
        GPIO.output(self.signal_pin, GPIO.HIGH)
        sleep(0.01)
        GPIO.output(self.signal_pin, GPIO.LOW)
        sleep(0.01)
        self.position -= 1
        return self.position

    def getPosition(self) -> int:
        return self.position
   
if __name__ == "__main__":
    stepper = StepperControl(40,38,36)
    while True:
        for _ in range(200):
            stepper.stepForward()
            sleep(0.01)
        for _ in range(200):
            stepper.stepBackward()
            sleep(0.01)
#1.8 degree per step
