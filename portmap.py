class PortMap:
    pass

motors = PortMap()

motors.left_drive = 8
motors.right_drive = 9
motors.left_intake = 3
motors.right_intake = 2
motors.claw = 5
motors.climb = 0
motors.elevator = 1

joysticks = PortMap()

joysticks.left_joystick = 0
joysticks.right_joystick = 1

joysticks.red_button_intake = 1
joysticks.blue_button_outtake = 2

joysticks.yellow_button_up_elevator = 3
joysticks.green_button_down_elevator = 4

joysticks.white_button_claw_up = 5
joysticks.white_button_claw_down = 6