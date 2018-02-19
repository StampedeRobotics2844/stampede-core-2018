from pyfrc.physics import drivetrains
import logging
import wpilib
import portmap
from networktables import NetworkTables
import math

logging.basicConfig(level=logging.DEBUG)

encoder_wheel_left = None

class PhysicsEngine:
    '''
    Simulate a motor 
    '''
    def __init__(self, physics_controller):
        self.physics_controller = physics_controller
        self.physics_controller.add_analog_gyro_channel(1)


    def update_sim(self, hal_data, now, tm_diff):
        '''
        called when the simulation parameters for the program need to be updated
        '''
        try:
            r_motor = hal_data['pwm'][9]['value']
            l_motor = hal_data['pwm'][8]['value']

            speed, rotation = drivetrains.two_motor_drivetrain(l_motor, r_motor)
            self.physics_controller.drive(speed, rotation, tm_diff)
        except:
            pass