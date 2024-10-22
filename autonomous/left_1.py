from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import logging
import portmap
import wpilib

logging.basicConfig(level=logging.DEBUG)

class LeftForward(StatefulAutonomous):
    MODE_NAME = 'Left Forward'

    def initialize(self):
        self.register_sd_var('drive_speed', 1)
        self.logger = logging.getLogger("Gladius")

    def getAverageEncoderPosition(self):
        return (self.encoder_wheel_left.getDistance() + self.encoder_wheel_right.getDistance()) / 2

    @state(first=True)
    def drive_forward(self):
        while self.getAverageEncoderPosition() < 50.0:
            self.drive.tankDrive(-0.5, -0.5)
            self.logger.log(logging.INFO, "distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
            self.logger.log(logging.INFO, "distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))

        
        self.drive.tankDrive(0,0)
