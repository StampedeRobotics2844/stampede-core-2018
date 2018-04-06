from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import logging
import portmap
import wpilib

logging.basicConfig(level=logging.DEBUG)


class TC(StatefulAutonomous):
    MODE_NAME = 'TR'

    def initialize(self):
        self.register_sd_var('drive_speed', 1)
        self.logger = logging.getLogger("Gladius")
        self.gameData = ''

    @timed_state(duration=2.5,next_state='drive_turn_or_forward',first=True)
    def start(self):
        self.drive.tankDrive(-1,-1)
        self.gameData = wpilib.DriverStation.getInstance().getGameSpecificMessage()

    @timed_state(duration=0.5,next_state='drive_claw_or_forward')
    def drive_turn_or_forward(self):
        if self.gameData[0] == 'R':
            self.drive.tankDrive(0.68, -0.69)
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(-1,-1)

        self.logger.log(logging.INFO, "gyro angle: {0}, game specific message: {1}".format(self.gyro.getAngle(), self.gameData))
        self.logger.log(logging.INFO, "distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
        self.logger.log(logging.INFO, "distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))
    
    @timed_state(duration=0.5,next_state='drive_turn')
    def drive_claw_or_forward(self):
        if self.gameData[0] == 'R':
            pass
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(-1,-1)

    @timed_state(duration=0.5,next_state='drive_forward')
    def drive_turn(self):
        if self.gameData[0] == 'R':
            pass
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(0.73,-0.73)

    @timed_state(duration=1, next_state='claw_up_or_forward')
    def drive_forward(self):
        if self.gameData[0] == 'R':
            self.drive.tankDrive(-0.5,-0.5)
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(-1,-1)

    @timed_state(duration=1, next_state='claw_out_or_forward')
    def claw_up_or_forward(self):
        if self.gameData[0] == 'R':
            self.elevator_motor.set(1)
            self.twoelevator_motor.set(1)
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(-1,-1)

    @timed_state(duration=0.7, next_state='drive_forward2')
    def claw_up_or_forward(self):
        if self.gameData[0] == 'R':
            self.elevator_motor.set(0)
            self.twoelevator_motor.set(0)
            self.claw_lintake_motor.set(-1)
            self.claw_rintake_motor.set(-1)
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(-1,-1)

    @timed_state(duration=1, next_state='drive_turn2')
    def drive_forward2(self):
        if self.gameData[0] == 'R':
            pass
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(-1,-1)

    @timed_state(duration=0.5,next_state='drive_forward3')
    def drive_turn2(self):
        if self.gameData[0] == 'R':
            pass
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(0.76,-0.76)
    
    @timed_state(duration=0.3, next_state='drive_claw_up')
    def drive_forward3(self):
        if self.gameData[0] == 'R':
            pass
        elif self.gameData[0] == 'L':
            self.drive.tankDrive(-0.9,-1)

    @timed_state(duration=1,next_state='drive_claw_out')
    def drive_claw_up(self):
        if self.gameData[0] == 'R':
            pass
        elif self.gameData[0] == 'L':
            self.elevator_motor.set(1)
            self.twoelevator_motor.set(1)

    @timed_state(duration=1)
    def drive_claw_out(self):
        if self.gameData[0] == 'R':
            pass
        elif self.gameData[0] == 'L':
            self.claw_lintake_motor.set(-1)
            self.claw_rintake_motor.set(-1)
            self.elevator_motor.set(0)
            self.twoelevator_motor.set(0)
