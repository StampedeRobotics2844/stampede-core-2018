'''
Steampede 2018
Betty H. Fairfax
Team 2844 @2018
bfhsroboticsclub@gmail.com
'''

import wpilib
import wpilib.drive
import logging
import portmap

from robotpy_ext.autonomous import StatefulAutonomous, timed_state
from networktables import NetworkTables
from robotpy_ext.autonomous import AutonomousModeSelector

logging.basicConfig(level=logging.DEBUG)

class StampedeRobot(wpilib.IterativeRobot):
    '''Main robot class'''
    def __init__(self):
        super().__init__()

        self.smart_dashboard = None
        self.motor_speed_stop = 0

        self.robot_speed = None
        self.intake_speed = None
        self.outake_speed = None
        self.elevator_speed_up = None
        self.elevator_speed_down = None
        self.claw_speed = None
        self.climber_speed = None

        self.drive_r_motor = None
        self.drive_l_motor = None

        self.claw_rintake_motor = None
        self.claw_lintake_motor = None

        self.elevator_motor = None
        self.climb_motor = None
        self.claw_motor = None

        self.left_stick = None
        self.right_stick = None
        

        self.drive = None

        self.gyro = None
        self.accel = None

    def robotInit(self):
        '''Robot-wide Initialization code'''
        #Initializing Smart Dashboard
        self.smart_dashboard = NetworkTables.getTable("SmartDashboard")

        #Initializing networktables
        self.smart_dashboard = NetworkTables.getTable("SmartDashboard")
        self.smart_dashboard.putNumber('robot_speed', 1)
        self.smart_dashboard.putNumber('intake_speed', 1)
        self.smart_dashboard.putNumber('outake_speed', 1)
        self.smart_dashboard.putNumber('elevator_speed_up', 1)
        self.smart_dashboard.putNumber('elevator_speed_down', 1)
        self.smart_dashboard.putNumber('claw_speed', 1)
        self.smart_dashboard.putNumber('climber_speed', 1)

        # initialize and launch the camera
        wpilib.CameraServer.launch()

        #Initalizing drive motors
        self.drive_l_motor = wpilib.Spark(portmap.motors.left_drive)
        self.drive_r_motor = wpilib.Spark(portmap.motors.right_drive)

        self.claw_lintake_motor = wpilib.Victor(portmap.motors.left_intake)
        self.claw_rintake_motor = wpilib.Victor(portmap.motors.right_intake)

        self.elevator_motor = wpilib.Spark(portmap.motors.elevator)

        self.climb_motor = wpilib.Victor(portmap.motors.climb)

        self.claw_motor = wpilib.Victor(portmap.motors.claw)

        # initialize drive
        self.drive = wpilib.drive.DifferentialDrive(self.drive_l_motor, self.drive_r_motor)
        self.drive.setExpiration(0.1)

        # joysticks 1 & 2 on the driver station
        self.left_stick = wpilib.Joystick(portmap.joysticks.left_joystick)
        self.right_stick = wpilib.Joystick(portmap.joysticks.right_joystick)

        # initialize gyro
        #self.gyro = wpilib.ADXRS450_Gyro()

        # initialize Accelerometer
        #self.accel = wpilib.ADXL345_I2C(wpilib.I2C.Port.kMXP,
        #    wpilib.ADXL345_SPI.Range.k2G)
  
        # initialize autonomous components
        self.components = {
            'drive': self.drive,
            'drive_r_motor': self.drive_r_motor,
            'drive_l_motor': self.drive_l_motor,
            'claw_rintake_motor': self.claw_rintake_motor,
            'claw_lintake_motor': self.claw_lintake_motor,
            'elevator_motor': self.elevator_motor
            'climb_motor': self.climb_motor
            'claw_motor': self.claw_motor
        }

        self.automodes = AutonomousModeSelector('autonomous', self.components)

    def autonomousInit(self):
        self.drive.setSafetyEnabled(True)

    def autonomousPeriodic(self):
        self.automodes.run()
        
    def disabledInit(self):
        '''Called only at the beginning of disabled mode'''
        pass
    
    def disabledPeriodic(self):
        '''Called every 20ms in disabled mode'''
        pass

    def teleopInit(self):
        '''Called only at the beginning of teleoperated mode'''
        self.drive.setSafetyEnabled(True)

    def teleopPeriodic(self):
        '''Called every 20ms in teleoperated mode'''
        
        try:

            if self.left_stick.getRawButton(portmap.joysticks.red_button_intake):
                self.claw_lintake_motor.set(1)
                self.claw_rintake_motor.set(1)
            elif self.right_stick.getRawButton(portmap.joysticks.blue_button_outtake):
                self.claw_lintake_motor.set(-1)
                self.claw_rintake_motor.set(-1)
            else:
                self.claw_lintake_motor.set(0)
                self.claw_rintake_motor.set(0)

            if self.left_stick.getRawButton(portmap.joysticks.yellow_button_up_elevator):
                self.elevator_motor.set(1)
            elif self.left_stick.getRawButton(portmap.joysticks.green_button_down_elevator):
                self.elevator_motor.set(-1)
            else:
                self.elevator_motor.set(0)
            
            if self.left_stick.getRawButton(portmap.joysticks.white_button_claw_up):
                self.claw_motor.set(1)
            elif self.left_stick.getRawButton(portmap.joysticks.white_button_claw_down):
                self.claw_motor.set(-1)
            else:
                self.claw_motor.set(0)

            self.drive.tankDrive(self.left_stick.getY(), self.right_stick.getY(), True)

        except:
            if not self.isFMSAttached():
                raise

    def isFMSAttached(self):
        return wpilib.DriverStation.getInstance().isFMSAttached()

if __name__ == '__main__':
    wpilib.run(StampedeRobot)
