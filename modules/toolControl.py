import RPi.GPIO as GPIO


class ToolControl():
    def __init__(self, pin: int) -> None:
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)

    def pick(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def place(self):
        GPIO.output(self.pin, GPIO.LOW)
       
    
if __name__ == "__main__":
    tool = ToolControl(9)
    from time import sleep
    while True:
        tool.pick()
        sleep(2)
        tool.place()
        sleep(2)
