from time import sleep
from modules import Vision, ToolControl, StepperControl, ConveyerControl
from configparser import ConfigParser
from RPi.GPIO import cleanup


class Robot():
    def __init__(self) -> None:
        # Reading Configuration File
        config = ConfigParser()
        config.read('./robot.ini')

        lead = float(config['motor-calibration']['lead'])
        step = float(config['motor-calibration']['step'])
        self.mm_to_step = 360/(lead*step)

        self.final_x_dest = int(
            config['final-destination']['x_position'])*(self.mm_to_step)
        self.final_y_dest = int(
            config['final-destination']['y_position'])*(self.mm_to_step)
        self.final_z_dest = int(
            config['final-destination']['z_position'])*(self.mm_to_step)

        # Initializing Peripherals
        self.robot_vision = Vision(
            config['Vision-calibration']['x_length'],
            config['Vision-calibration']['y_length'],
            config['Vision-calibration']['circle_diameter'])

        self.x_motor = StepperControl(5, 5, 5)
        self.x_motor_position = 0

        self.y_motor = StepperControl(5, 5, 5)
        self.y_motor_position = 0

        self.z_motor = StepperControl(5, 5, 5)
        self.z_motor_position = 0

        self.tool = ToolControl(6)

        self.conveyer = ConveyerControl(7)
        # Starting The Robot Loop
        while True:
            self.robotLoop()

    def robotLoop(self) -> None:

        circle = self.robot_vision.findCircle()
        # TODO: change the code for getting positions
        if circle == None:
            self.conveyer.load()
            return
        x_position = circle[0]
        y_position = circle[1]
        x_position = x_position*(self.mm_to_step)
        y_position = y_position*(self.mm_to_step)
        x_position_reached = False
        y_position_reached = False
        while (not x_position_reached) or (not y_position_reached):
            if(self.x_motor_position > x_position):
                self.x_motor_position = self.x_motor.stepBackward()
            elif (self.x_motor_position < x_position):
                self.x_motor_position = self.x_motor.stepForward()
            else:
                x_position_reached = True

            if(self.y_motor_position > y_position):
                self.y_motor_position = self.y_motor.stepBackward()
            elif (self.y_motor_position < y_position):
                self.y_motor_position = self.y_motor.stepForward()
            else:
                y_position_reached = True
        sleep(0.5)
        # Reached to position
        z_position_reached = False
        while (not z_position_reached):
            if(self.z_motor_position < self.z_position):
                self.z_motor.stepForward()
            else:
                z_position_reached = True
        sleep(0.5)
        self.tool.pick()
        sleep(0.5)
        z_position_reached = False
        while (not z_position_reached):
            if(self.z_motor_position > 0):
                self.z_motor.stepBackward()
            else:
                z_position_reached = True

        x_position_reached = False
        y_position_reached = False
        while (not x_position_reached) or (not y_position_reached):
            if(self.x_motor_position > self.final_x_dest):
                self.x_motor_position = self.x_motor.stepBackward()
            elif (self.x_motor_position < self.final_x_dest):
                self.x_motor_position = self.x_motor.stepForward()
            else:
                x_position_reached = True

            if(self.y_motor_position > self.final_y_dest):
                self.y_motor_position = self.y_motor.stepBackward()
            elif (self.y_motor_position < self.final_y_dest):
                self.y_motor_position = self.y_motor.stepForward()
            else:
                y_position_reached = True
        sleep(0.5)
        z_position_reached = False
        while (not z_position_reached):
            if(self.z_motor_position < self.final_z_dest):
                self.z_motor.stepForward()
            else:
                z_position_reached = True
        sleep(0.5)
        self.tool.place()
        sleep(0.5)
        z_position_reached = False
        while (not z_position_reached):
            if(self.z_motor_position < 0):
                self.z_motor.stepBackward()
            else:
                z_position_reached = True


def sigintHandler(signal, frame):
    print('Exiting the program.')
    cleanup()
    sys.exit(0)


if __name__ == "__main__":
    import sys
    import signal
    signal.signal(signal.SIGINT, sigintHandler)
    Robot()
