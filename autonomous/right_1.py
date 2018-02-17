from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state


class RightForward(StatefulAutonomous):
    MODE_NAME = 'Right Forward'

    def initialize(self):
        self.register_sd_var('drive_speed', 1)

    @state(first=True)
    def drive_forward(self):
        self.drive.tankDrive(leftValue=-0.5, rightValue=-0.5)
