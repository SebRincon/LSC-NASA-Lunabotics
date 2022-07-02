import pygame

def startInput():
    pygame.init()

    # waiting for user to plug in controller
    # connecting to controller and initialize

    xboxcontroller = pygame.joystick.Joystick(0)
    xboxcontroller.init()

    # starting loop to obtain x and y controller analog values
    # creating variables to hold x and y value from controller
    left_analog_y_value = 0.0
    right_analog_x_value = 0.0
    up_dpad_value = 0.0

    while True:
        pygame.event.get()

        # storing analog input from x and y by converting to type float
        left_analog_y_value = float(format(xboxcontroller.get_axis(1)))
        right_analog_x_value = float(format(xboxcontroller.get_axis(2)))
        #button A
        #a_button_value = float(format(xboxcontroller.get_button(0)))
        #button Y
        #y_button_value = float(format(xboxcontroller.get_button(3)))
        #dpad_value
        #dpad_value = (format(xboxcontroller.get_hat(0)))


        print(f'up_dpad_value {up_dpad_value}')

if __name__ == 'main':
    runner = startInput()
    runner.startInput()

    # Reverse the commenting for these two to change control type
    # runner.keyboardTest()