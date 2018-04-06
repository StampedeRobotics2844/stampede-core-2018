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

        self.logger = logging.getLogger("Gladius")

        self.smart_dashboard = None
        self.motor_speed_stop = 0

        self.gameData = None

        self.robot_speed = None
        self.intake_speed = None
        self.outake_speed = None
        self.elevator_speed_up = None
        self.elevator_speed_down = None
        self.claw_speed = None
        self.climber_speed = None

        self.kDistancePerRevolution = 18.84
        self.kPulsesPerRevolution = 1440
        self.kDistancePerPulse = self.kDistancePerRevolution / self.kPulsesPerRevolution

        self.drive_r_motor = None
        self.drive_l_motor = None

        self.claw_rintake_motor = None
        self.claw_lintake_motor = None

        self.elevator_motor = None
        self.twoelevator_motor = None
        self.climb_motor = None
        self.claw_motor = None

        self.left_stick = None
        self.right_stick = None
        
        self.encoder_wheel_left = None
        self.encoder_wheel_right = None
        self.encoder_lift = None

        self.drive = None

        self.address= 0x53

        self.range = None
        self.rangeU = None
        self.gyro = None
        self.accel = None

        self.intake = False

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

        self.encoder_wheel_left = wpilib.Encoder(0,1,True,wpilib.Encoder.EncodingType.k4X)
        self.encoder_wheel_right = wpilib.Encoder(2,3,False,wpilib.Encoder.EncodingType.k4X)
        self.encoder_lift = wpilib.Encoder(4,5,True,wpilib.Encoder.EncodingType.k4X)

        self.encoder_wheel_left.setDistancePerPulse(self.kDistancePerPulse)
        self.encoder_wheel_right.setDistancePerPulse(self.kDistancePerPulse)
        self.encoder_lift.setDistancePerPulse(self.kDistancePerPulse)

        #Initalizing drive motors
        self.drive_l_motor = wpilib.Spark(portmap.motors.left_drive)
        self.drive_r_motor = wpilib.Spark(portmap.motors.right_drive)

        self.claw_lintake_motor = wpilib.Victor(portmap.motors.left_intake)
        self.claw_rintake_motor = wpilib.Victor(portmap.motors.right_intake)

        self.elevator_motor = wpilib.Spark(portmap.motors.elevator)
        self.twoelevator_motor = wpilib.Victor(portmap.motors.twoelevator)

        self.climb_motor = wpilib.Victor(portmap.motors.climb)
        self.claw_motor = wpilib.Victor(portmap.motors.claw)

        # initialize drive
        self.drive = wpilib.drive.DifferentialDrive(self.drive_l_motor, self.drive_r_motor)
        self.drive.setExpiration(0.1)

        # joysticks 1 & 2 on the driver station
        self.left_stick = wpilib.Joystick(portmap.joysticks.left_joystick)
        self.right_stick = wpilib.Joystick(portmap.joysticks.right_joystick)

        # initialize gyro
        self.gyro = wpilib.ADXRS450_Gyro(wpilib.SPI.Port.kOnboardCS2)

        self.range = wpilib.AnalogInput(0)

        #self.rangeU = wpilib.Ultrasonic(0, 0)

        # initialize Accelerometer
        #self.accel = wpilib.ADXL345_I2C(wpilib.I2C.Port.kMXP,wpilib.ADXL345_I2C.Range.k16G,0x1D)
  
        # initialize autonomous components
        self.components = {
            'drive': self.drive,
            'drive_r_motor': self.drive_r_motor,
            'drive_l_motor': self.drive_l_motor,
            'claw_rintake_motor': self.claw_rintake_motor,
            'claw_lintake_motor': self.claw_lintake_motor,
            'elevator_motor': self.elevator_motor,
            'twoelevator_motor': self.twoelevator_motor,
            'climb_motor': self.climb_motor,
            'claw_motor': self.claw_motor,
            'encoder_wheel_left' : self.encoder_wheel_left,
            'encoder_wheel_right' : self.encoder_wheel_right,
            'gyro' : self.gyro,
            'range' : self.range,
            'gameData' : self.gameData
        }

        self.automodes = AutonomousModeSelector('autonomous', self.components)

    def getDistance(self):
        '''
        [(Vcc/1024) = Vi]
        Vcc = Supplied Voltage
        Vi = Volts per 5 mm (Scaling)
        
        Example 1: Say you have an input voltage of +5.0V the formula would read:
        [(5.0V/1024) = 0.004883V per 5 mm = 4.883mV per 5 mm]
        
        Calculating the Range
        Once you know the voltage scaling it is easy to properly calculate the range.
        
        The range formula is:
        [5*(Vm/Vi) = Ri]
        Vm = Measured Voltage
        Ri = Range in mm
        Vi = Volts per 5 mm (Scaling)
        '''

        voltage_scaling = 5.0/1024
        measured_voltages = self.range.getVoltage()
        distance = 5 * (measured_voltages/voltage_scaling)
        mmToInchScaling = 0.03937007874

        self.logger.log(logging.INFO, "measured voltage: {0}, distance: {1} mm, distnace: {2} inches".format(measured_voltages, distance, distance*mmToInchScaling))

        return distance

    def clawIntake(self):
        self.claw_lintake_motor.set(0.55)
        self.claw_rintake_motor.set(0.55)

    def clawOutake(self):
        self.claw_lintake_motor.set(-1)
        self.claw_rintake_motor.set(-1) 

    def clawStopTake(self):
        self.claw_lintake_motor.set(0)
        self.claw_rintake_motor.set(0) 

    def liftUp(self):
        self.elevator_motor.set(1)
        self.twoelevator_motor.set(1) 

    def liftDown(self):
        self.elevator_motor.set(-1)
        self.twoelevator_motor.set(-1)
    
    def liftStop(self):
        self.elevator_motor.set(0)
        self.twoelevator_motor.set(0)

    def clawRUp(self):
        self.claw_motor.set(1)

    def clawRDown(self):
        self.claw_motor.set(-1)

    def clawRStop(self):
        self.claw_motor.set(0)

    def autonomousInit(self):
        self.drive.setSafetyEnabled(True)
        self.gyro.calibrate()
        self.gameData = self.getGameSpecificData()
        self.logger.log(logging.INFO, "Game Data: {0}".format(self.gameData))

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
        self.encoder_wheel_left.reset()
        self.encoder_wheel_right.reset()
        self.encoder_lift.reset()
        self.gyro.calibrate()

    def teleopPeriodic(self):
        '''Called every 20ms in teleoperated mode'''
        
        try:
            
            if self.left_stick.getRawButton(portmap.joysticks.red_button_intake):
                self.clawIntake()
            elif self.left_stick.getRawButton(portmap.joysticks.blue_button_outtake):
                self.clawOutake()
            else:
                self.clawStopTake()

            if self.left_stick.getRawButton(portmap.joysticks.yellow_button_up_elevator):
                self.liftUp()
            elif self.left_stick.getRawButton(portmap.joysticks.green_button_down_elevator):
                self.liftDown()
            else:
                self.liftStop()
            
            if self.left_stick.getRawButton(portmap.joysticks.white_button_claw_up):
                self.clawRUp()
            elif self.left_stick.getRawButton(portmap.joysticks.white_button_claw_down):
                self.clawRDown()
            else:
                self.clawRStop()

            self.drive.tankDrive(self.left_stick.getY() * 0.7, self.right_stick.getY() * 0.7, False)

        except:
            if not self.isFMSAttached():
                raise

        self.logger.log(logging.INFO, "distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
        self.logger.log(logging.INFO, "distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))
        #self.logger.log(logging.INFO, "distance lift: {0}".format(self.encoder_lift.getDistance()))
        self.logger.log(logging.INFO, "gyro angle: {0}".format(self.gyro.getAngle()))
        self.logger.log(logging.INFO, "range: {0}".format(self.getDistance()))
        #self.logger.log(logging.INFO, "accel x, y, z: {0}, {1}, {2}".format(self.accel.getX(), self.accel.getY(), self.accel.getZ()))

    def isFMSAttached(self):
        return wpilib.DriverStation.getInstance().isFMSAttached()

    def getGameSpecificData(self):
        return wpilib.DriverStation.getInstance().getGameSpecificMessage()

if __name__ == '__main__':
    wpilib.run(StampedeRobot)
