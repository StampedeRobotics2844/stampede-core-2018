class PortMap:
    pass

motors = PortMap()

motors.left_drive = 8 #black
motors.right_drive = 9 #purple
motors.left_intake = 3 #red
motors.right_intake = 2 #green
motors.claw = 5
motors.climb = 0
motors.elevator = 1 #yellow
motors.twoelevator = 4 #blue

joysticks = PortMap()

joysticks.left_joystick = 0
joysticks.right_joystick = 1

joysticks.red_button_intake = 1
joysticks.blue_button_outtake = 2

joysticks.yellow_button_up_elevator = 3
joysticks.green_button_down_elevator = 4

joysticks.white_button_claw_up = 5
joysticks.white_button_claw_down = 6