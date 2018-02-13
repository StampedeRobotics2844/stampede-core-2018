'''
Steampede 2018
Betty H. Fairfax
Team 2844 @2018
bfhsroboticsclub@gmail.com
'''

import wpilib
import wpilib.drive
import logging

from networktables import NetworkTables
from robotpy_ext.autonomous import AutonomousModeSelector

logging.basicConfig(level=logging.DEBUG)

class StampedeRobot(wpilib.IterativeRobot):
    '''Main robot class'''
    def __init__(self):
        super().__init__()

        self.smart_dashboard = None

        self.drive_r_motor = None
        self.drive_l_motor = None

        self.left_stick = None
        self.right_stick = None

        self.drive = None

        self.gyro = None
        self.accel = None

    def robotInit(self):
        '''Robot-wide Initialization code'''
        #Initializing Smart Dashboard
        self.smart_dashboard = NetworkTables.getTable("SmartDashboard")

        # initialize and launch the camera
        wpilib.CameraServer.launch()

        #Initalizing drive motors
        self.drive_r_motor = wpilib.Spark(9)
        self.drive_l_motor = wpilib.Spark(8)

        # initialize drive
        self.drive = wpilib.drive.DifferentialDrive(self.drive_l_motor, self.drive_r_motor)
        self.drive.setExpiration(0.1)

        # joysticks 1 & 2 on the driver station
        self.left_stick = wpilib.Joystick(0)
        self.right_stick = wpilib.Joystick(1)

        # initialize gyro
        self.gyro = wpilib.ADXRS450_Gyro()

        # initialize Accelerometer
        #self.accel = wpilib.ADXL345_I2C(wpilib.I2C.Port.kMXP,
        #    wpilib.ADXL345_SPI.Range.k2G)


    def autonomousInit(self):
        '''Called only at the beginning'''
        pass

    def autonomousPeriodic(self):
        '''Called ever 20ms'''
        pass
        
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
            self.drive.tankDrive(self.left_stick.getY(), self.right_stick.getY(), True)
        except:
            if not self.isFMSAttached():
                raise

    def isFMSAttached(self):
        return wpilib.DriverStation.getInstance().isFMSAttached()

if __name__ == '__main__':
    wpilib.run(StampedeRobot)
