from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state


class RightForward(StatefulAutonomous):
    MODE_NAME = 'Right Forward'

    def initialize(self):
        self.register_sd_var('drive_speed', 1)

    def getAverageEncoderPosition(self):
        return (self.encoder_wheel_left.getDistance() + self.encoder_wheel_right.getDistance()) / 2

    @state(first=True)
    def drive_forward(self):
        while self.getAverageEncoderPosition() < 50.0:
            self.drive.tankDrive(-0.5, -0.5)
        
        self.drive.tankDrive(0,0)
