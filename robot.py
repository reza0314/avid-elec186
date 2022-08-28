from time import sleep
from modules import Vision, ToolControl, StepperControl, ConveyerControl
from configparser import ConfigParser
from RPi.GPIO import cleanup, setwarnings


# test all three dimentions of the robot
# test the pick and place mechanism
# test loading mechanism

class Robot():
    def __init__(self) -> None:
        # Reading Configuration File
        config = ConfigParser()
        config.read('./robot.ini')

        lead = float(config['motor-calibration']['lead'])
        step = float(config['motor-calibration']['step'])
        self.sleep_time = float(config['delays']['normal_delay'])
        self.mm_to_step = 360/(lead*step)

        self.final_x_dest = int(
            config['final-destination']['x_position'])*(self.mm_to_step)
        self.final_y_dest = int(
            config['final-destination']['y_position'])*(self.mm_to_step)
        self.final_z_dest = int(
            config['final-destination']['z_position'])*(self.mm_to_step)
        self.z_direction_distance = float(
            config['motor-calibration']['z_direction_distance'])

        # Initializing Peripherals
        try:
            self.robot_vision = Vision(
                int(config['Vision-calibration']['x_length']),
                int(config['Vision-calibration']['y_length']),
                int(config['Vision-calibration']['circle_diameter']))
        except:
            while True:
                print("Camera Error!")
                sleep(10)

        self.x_motor = StepperControl(int(config['GPIOS']['x_stepper_signal_pin']),
                                      int(config['GPIOS']
                                          ['x_stepper_direction_pin']),
                                      int(config['GPIOS']['x_stepper_limit_switch_pin']))
        self.x_motor_position = 0
        self.x_motor.calibrate_motor()
        self.y_motor = StepperControl(int(config['GPIOS']['y_stepper_signal_pin']),
                                      int(config['GPIOS']
                                          ['y_stepper_direction_pin']),
                                      int(config['GPIOS']['y_stepper_limit_switch_pin']))
        self.y_motor_position = 0
        # self.y_motor.clibrate_motor()
        self.z_motor = StepperControl(int(config['GPIOS']['z_stepper_signal_pin']),
                                      int(config['GPIOS']
                                          ['z_stepper_direction_pin']),
                                      int(config['GPIOS']['z_stepper_limit_switch_pin']))
        self.z_motor_position = 0
        # self.z_motor.clibrate_motor()
        self.tool = ToolControl(int(config['GPIOS']['tool_relay_pin']))

        self.conveyer = ConveyerControl(
            int(config['GPIOS']['conveyer_relay_pin']), float(config['delays']['load_delay']))
        self.circles = []
        sleep(2)
        print("initialization done")

        # Starting The Robot Loop
        # comment these three lines and un comment self.test()
        while True:
            self.robotLoop()
            sleep(2)
        # self.test()

    def test(self) -> None:
        
        sleep(3)
        x_position = 300
        # y_position = 50
        # code for the y motor
        x_position_reached = False
        # print('Test')

        while (not x_position_reached):
            # add code for y motor
            if(self.x_motor_position > x_position):
                self.x_motor_position = self.x_motor.stepBackward()
            elif (self.x_motor_position < x_position):
                self.x_motor_position = self.x_motor.stepForward()
            else:
                x_position_reached = True
            # print(self.x_motor.position)
        # add code for picking the ceramics
        # go to final destnations
        x_position = 100
        x_position_reached = False
        while (not x_position_reached):
            #add code for y motor also
            if(self.x_motor_position > x_position):
                self.x_motor_position = self.x_motor.stepBackward()
            elif (self.x_motor_position < x_position):
                self.x_motor_position = self.x_motor.stepForward()
            else:
                x_position_reached = True
            # print(self.x_motor.position)
        # add code for placing compunents
        # add code for reloading

    def robotLoop(self) -> None:

        self.circles = self.robot_vision.findCircles()
        if self.circles == None:
            print("No ceramics found, reloading...")
            self.conveyer.load()
            return
        circle = self.circles.pop(0)
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
        sleep(self.sleep_time)
        # Reached to position
        z_position_reached = False
        while (not z_position_reached):
            if(self.z_motor_position < self.z_direction_distance):
                self.z_motor.stepForward()
            else:
                z_position_reached = True
        sleep(self.sleep_time)
        self.tool.pick()
        sleep(self.sleep_time)
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
        sleep(self.sleep_time)
        z_position_reached = False
        while (not z_position_reached):
            if(self.z_motor_position < self.final_z_dest):
                self.z_motor.stepForward()
            else:
                z_position_reached = True
        sleep(self.sleep_time)
        self.tool.place()
        sleep(self.sleep_time)
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
    setwarnings(False)
    signal.signal(signal.SIGINT, sigintHandler)
    print("here")
    Robot()
