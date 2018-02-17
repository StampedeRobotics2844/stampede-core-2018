from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state


class CenterForward(StatefulAutonomous):
    MODE_NAME = 'Center Forward'

    def initialize(self):
        self.register_sd_var('drive_speed', 1)

    @state(first=True)
    def drive_forward(self):
        self.drive.tankDrive(leftValue=-0.5, rightValue=-0.5)