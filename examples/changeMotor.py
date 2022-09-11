'''
The example is started from line 55 in this programm motors go in opposite direction then
then same direction then the program ends

To change the the motor to other simply just chage y_motor to x_motor
or add somthing like y_motor.stepBackward or x_motor.stepForward or ...
In other words you have to change or add the names like x_motor , y_motor followed by a dot
then the direction stepBackward or stepForward followed by ().
            x_motor.stepBackward()
            {name}.{direction}()
'''
import RPi.GPIO as GPIO
from time import sleep

class StepperControl():

    def __init__(self, signal_pin: int, direction_pin: int, limit_switch_pin: int) -> None:
        self.signal_pin = signal_pin
        self.direction_pin = direction_pin
        self.limit_switch_pin = limit_switch_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.signal_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.limit_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.position = 0
        self.calibrate_motor()

    def calibrate_motor(self) -> None:
        while GPIO.input(self.limit_switch_pin):
            self.stepBackward()
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
    print("Start")
    x_motor = StepperControl(40,38,36)
    y_motor = StepperControl(37,35,33)
    print("Objects created")
    sleep(2)
    print("Motors must go in opposite direction")
    for _ in range(20):
        x_motor.stepForward()
        y_motor.stepBackward()
        sleep(20)
    for _ in range(200):
        y_motor.stepForward()
        x_motor.stepBackward()
        sleep(20)
    
    sleep(2)
    print("Motors must go in same direction")
    for _ in range(20):
        x_motor.stepForward()
        y_motor.stepForward()
        sleep(20)
    for _ in range(200):
        y_motor.stepBackward()
        x_motor.stepBackward()
        sleep(20)
    sleep(2)
    print("Program ends")