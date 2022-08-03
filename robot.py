from time import sleep
from modules import Vision, ToolControl, StepperControl, ConveyerControl
from configparser import ConfigParser


class Robot():
    def __init__(self) -> None:
        # Reading Configuration File
        config = ConfigParser()
        config.read('./robot.ini')

        # Initializing Peripherals
        self.robot_vision = Vision(
            config['Vision-calibration']['x_length'],
            config['Vision-calibration']['y_length'],
            config['Vision-calibration']['circle_diameter'])

        self.x_motor = StepperControl(5, 5, 5)
        self.x_motor_position = 0

        # Starting The Robot Loop
        while True:
            self.robotLoop()

    def robotLoop(self) -> None:
        
        # self.robot_vision.test()
        # TODO: change the code for getting positions
        x_position = 200
        x_position_reached = False
        while (not x_position_reached):
            if(self.x_motor_position != x_position):
                self.x_motor_position = self.x_motor.test()
            else:
                x_position_reached = True
            sleep(0.01)
        


def sigintHandler(signal, frame):
    print('Interrupted')
    sys.exit(0)

if __name__ == "__main__":
    import sys
    import signal
    signal.signal(signal.SIGINT, sigintHandler)
    Robot()
