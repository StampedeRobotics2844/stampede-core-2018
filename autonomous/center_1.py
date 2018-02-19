from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import logging
import portmap
import wpilib

logging.basicConfig(level=logging.DEBUG)


class CenterForward(StatefulAutonomous):
    MODE_NAME = 'Center Forward'

    def initialize(self):
        self.register_sd_var('drive_speed', 1)
        self.logger = logging.getLogger("Gladius")
        self.kDistancePerRevolution = 18.84
        self.kPulsesPerRevolution = 1440
        self.kDistancePerPulse = self.kDistancePerRevolution / self.kPulsesPerRevolution
        self.encoder_wheel_left.setDistancePerPulse(self.kDistancePerPulse)
        self.encoder_wheel_right.setDistancePerPulse(self.kDistancePerPulse)

    def init(self):
        self.encoder_wheel_left = wpilib.Encoder(0,1,True,wpilib.Encoder.EncodingType.k4X)
        self.encoder_wheel_right = wpilib.Encoder(2,3,False,wpilib.Encoder.EncodingType.k4X)
    
    def getRTurnEncoderPosition(self):
        return (-self.encoder_wheel_left.getDistance() + self.encoder_wheel_right.getDistance()) / 2
    
    def getAverageEncoderPosition(self):
        return (self.encoder_wheel_left.getDistance() + self.encoder_wheel_right.getDistance()) / 2

    @state(first=True)
    def drive_turn_right(self):

        while self.getRTurnEncoderPosition() < 7.0:
            self.drive.tankDrive(-0.5, 0.5)
            self.logger.log(logging.INFO, "distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
            self.logger.log(logging.INFO, "distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))
        
        if self.getRTurnEncoderPosition() > 7.0:
            self.drive.tankDrive(0,0)
            self.encoder_wheel_left.reset()
            self.encoder_wheel_right.reset()
            self.next_state('drive_forward')
    
    @state()
    def drive_forward(self):
        while self.getAverageEncoderPosition() < 50.0:
            self.drive.tankDrive(-0.5, -0.5)
            self.logger.log(logging.INFO, "distance wheel left: {0}".format(self.encoder_wheel_left.getDistance()))
            self.logger.log(logging.INFO, "distance wheel right: {0}".format(self.encoder_wheel_right.getDistance()))
        
        self.drive.tankDrive(0,0)
