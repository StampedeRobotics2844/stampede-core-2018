from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import logging
import portmap
import wpilib

logging.basicConfig(level=logging.DEBUG)


class TCenterForward(StatefulAutonomous):
    MODE_NAME = 'Timed Center Forward'

    def initialize(self):
        self.register_sd_var('drive_speed', 1)
        self.logger = logging.getLogger("Gladius")

    @timed_state(duration=0.5,first=True,next_state='drive_forward')
    def drive_turn_right(self):
        self.drive.tankDrive(-0.6, 0.5)
    
    @timed_state(duration=2.2,next_state='drive_turn_left')
    def drive_forward(self):
        self.drive.tankDrive(-1, -1)

    @timed_state(duration=0.5,next_state='drive_forward2')
    def drive_turn_left(self):
        self.drive.tankDrive(0.5,-0.6)

    @timed_state(duration=0.7)
    def drive_forward2(self):
        self.drive.tankDrive(-1,-1)
