from modules import Vision, ToolControl, StepperControl, ConveyerControl
from configparser import ConfigParser


class Robot():
    robot_vision = ...

    def __init__(self) -> None:
        # Reading Configuration File
        config = ConfigParser()
        config.read('./robot.ini')

        # Initializing Peripherals
        self.robot_vision = Vision(
            config['Vision-calibration']['x_length'],
            config['Vision-calibration']['y_length'],
            config['Vision-calibration']['circle_diameter'])

        # Starting The Robot Loop
        self.robotLoop()

    def robotLoop(self):
        self.robot_vision.test()
        pass


if __name__ == "__main__":
    Robot()
