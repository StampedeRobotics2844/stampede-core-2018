from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import logging
import portmap
import wpilib

logging.basicConfig(level=logging.DEBUG)

class TLeftForward(StatefulAutonomous):
    MODE_NAME = 'Timed Left Forward'

    def initialize(self):
        self.register_sd_var('drive_speed', 1)
        self.logger = logging.getLogger("Gladius")

    @timed_state(duration=3,first=True)
    def drive_forward(self):
        self.drive.tankDrive(-1, -1)
