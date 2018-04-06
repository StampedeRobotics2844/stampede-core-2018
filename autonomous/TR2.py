from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import logging
import portmap
import wpilib

logging.basicConfig(level=logging.DEBUG)


class TC(StatefulAutonomous):
    MODE_NAME = 'TR2'

    def initialize(self):
        self.register_sd_var('drive_speed', 1)
        self.logger = logging.getLogger("Gladius")
        self.gameData = ''

    @timed_state(duration=2.5,next_state='drive_turn_or_forward',first=True)
    def start(self):
        self.drive.tankDrive(-1,-1)
        self.gameData = wpilib.DriverStation.getInstance().getGameSpecificMessage()

    @timed_state(duration=0.5,next_state='drive_forward')
    def drive_turn_or_forward(self):
        if self.gameData[0] == 'R':
            self.drive.tankDrive(0.74, -0.74)
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(-1,-1)

        self.logger.log(logging.INFO, "gyro angle: {0}, game specific message: {1}".format(self.gyro.getAngle(), self.gameData))
        self.logger.log(logging.INFO, "distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
        self.logger.log(logging.INFO, "distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))
    
    @timed_state(duration=0.5,next_state='drive_claw_up_or_turn')
    def drive_forward(self):
        if self.gameData[0] == 'R':
            self.drive.tankDrive(-0.7,-0.7)
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(-1,-1)

    @timed_state(duration=0.5,next_state='claw_or_forward')
    def drive_claw_up_or_turn(self):
        if self.gameData[0] == 'R':
            self.elevator_motor.set(1)
            self.twoelevator_motor.set(1)
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(-1,-1)

    @timed_state(duration=0.5)
    def claw_or_forward(self):
        if self.gameData[0] == 'R':
            self.claw_lintake_motor.set(-1)
            self.claw_rintake_motor.set(-1)
            self.elevator_motor.set(0)
            self.twoelevator_motor.set(0)
        elif self.gameData[0] == 'L':
            pass

