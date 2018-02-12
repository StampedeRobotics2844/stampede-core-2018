import wpilib

class StampedeRobot(wpilib.IterativeRobot):
    '''Main robot class'''

    def RobotInit(self):
        '''Robot-wide Initialization code'''

        self.lstick = wpilib.joystick
        self.lstick = wpilib.spark
        self.lstick = wpilib.victor

    def autonomousInit(self):
        '''Called only at the beginning'''
        pass
        
    def disabledInit(self):
        '''Called only at the beginning of disabled mode'''
        pass
    
    def disabledPeriodic(self):
        '''Called every 20ms in disabled mode'''
        pass

    def teleopInit(self):
        '''Called only at the beginning of teleoperated mode'''
        pass

    def teleopPeriodic(self):
        '''Called every 20ms in teleoperated mode'''
        
        # Move a motor with a Joystick
        self.motor.set(self.lstick.getY())

if __name__ == '__main__':
    wpilib.run(MyRobot)
