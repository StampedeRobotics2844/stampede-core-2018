from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import logging
import portmap
import wpilib

logging.basicConfig(level=logging.DEBUG)


class TC(StatefulAutonomous):
    MODE_NAME = 'TC'

    def initialize(self):
        self.register_sd_var('drive_speed', 1)
        self.logger = logging.getLogger("Gladius")
        self.gameData = ''
        self.time = wpilib.DriverStation.getInstance().getMatchTime()

    @timed_state(duration=0.2,next_state='drive_turn',first=True)
    def start(self):
        self.drive.tankDrive(-1,-1)
        
        self.logger.log(logging.INFO, "1.gyro angle: {0}, game specific message: {1}".format(self.gyro.getAngle(), self.gameData))
        self.logger.log(logging.INFO, "1.distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
        self.logger.log(logging.INFO, "1.distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))

    @timed_state(duration=0.5,next_state='drive_forward')
    def drive_turn(self):
        self.gameData = wpilib.DriverStation.getInstance().getGameSpecificMessage()

        if self.gameData[0] == 'R':
            self.drive.tankDrive(-0.6, 0.5)
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(0.5,-0.6)

        self.logger.log(logging.INFO, "2.gyro angle: {0}, game specific message: {1}".format(self.gyro.getAngle(), self.gameData))
        self.logger.log(logging.INFO, "2.distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
        self.logger.log(logging.INFO, "2.distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))
    
    @timed_state(duration=2.3,next_state='drive_turn_2')
    def drive_forward(self):
        self.drive.tankDrive(-1,-1)

        self.logger.log(logging.INFO, "3.gyro angle: {0}, game specific message: {1}".format(self.gyro.getAngle(), self.gameData))
        self.logger.log(logging.INFO, "3.distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
        self.logger.log(logging.INFO, "3.distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))

    @timed_state(duration=0.5,next_state='drive_forward2')
    def drive_turn_2(self):
        if self.gameData[0] == 'R':
            self.drive.tankDrive(0.5,-0.6)
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(-0.6,0.5)

        self.logger.log(logging.INFO, "4.gyro angle: {0}, game specific message: {1}".format(self.gyro.getAngle(), self.gameData))
        self.logger.log(logging.INFO, "4.distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
        self.logger.log(logging.INFO, "4.distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))

    @timed_state(duration=0.7,next_state='drive_turn_3')
    def drive_forward2(self):
        self.drive.tankDrive(-1,-1)

        self.logger.log(logging.INFO, "5.gyro angle: {0}, game specific message: {1}".format(self.gyro.getAngle(), self.gameData))
        self.logger.log(logging.INFO, "5.distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
        self.logger.log(logging.INFO, "5.distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))

    @timed_state(duration=0.6,next_state='drive_forward3')
    def drive_turn_3(self):
        if self.gameData[0] == 'R':
            self.drive.tankDrive(0.7,-0.7)
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(-0.7,0.7)

        self.logger.log(logging.INFO, "6.gyro angle: {0}, game specific message: {1}".format(self.gyro.getAngle(), self.gameData))
        self.logger.log(logging.INFO, "6.distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
        self.logger.log(logging.INFO, "6.distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))

    @timed_state(duration=0.2,next_state='drive_claw_up')
    def drive_forward3(self):
        if self.gameData[0] == 'R':
            self.drive.tankDrive(-1,-1)
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(-0.5,-0.5)

        self.logger.log(logging.INFO, "7.gyro angle: {0}, game specific message: {1}".format(self.gyro.getAngle(), self.gameData))
        self.logger.log(logging.INFO, "7.distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
        self.logger.log(logging.INFO, "7.distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))

    @timed_state(duration=1,next_state='claw_out')
    def drive_claw_up(self):
        if self.gameData[0] == 'R':
            self.elevator_motor.set(1)
            self.twoelevator_motor.set(1)
        elif self.gameData[0] == 'L':
            self.elevator_motor.set(1)
            self.twoelevator_motor.set(1)

        self.logger.log(logging.INFO, "8.gyro angle: {0}, game specific message: {1}".format(self.gyro.getAngle(), self.gameData))
        self.logger.log(logging.INFO, "8.distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
        self.logger.log(logging.INFO, "8.distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))

    @timed_state(duration=1)
    def claw_out(self):
        if self.gameData[0] == 'R':
            self.claw_lintake_motor.set(-1)
            self.claw_rintake_motor.set(-1)
            self.elevator_motor.set(0)
            self.twoelevator_motor.set(0)
        elif self.gameData[0] == 'L':
            self.claw_lintake_motor.set(-1)
            self.claw_rintake_motor.set(-1)
            self.elevator_motor.set(0)
            self.twoelevator_motor.set(0)

        self.logger.log(logging.INFO, "9.gyro angle: {0}, game specific message: {1}".format(self.gyro.getAngle(), self.gameData))
        self.logger.log(logging.INFO, "9.distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
        self.logger.log(logging.INFO, "9.distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))