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
    
    def getRTurnEncoderPosition(self):
        return (self.encoder_wheel_left.getDistance() - self.encoder_wheel_right.getDistance()) / 2

    def getAverageEncoderPosition(self):
        return (self.encoder_wheel_left.getDistance() + self.encoder_wheel_right.getDistance()) / 2

    @timed_state(duration=3,first=True)
    def drive_forward(self):
        self.drive.tankDrive(-1, -1)
        self.logger.log(logging.INFO, "distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
        self.logger.log(logging.INFO, "distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))

