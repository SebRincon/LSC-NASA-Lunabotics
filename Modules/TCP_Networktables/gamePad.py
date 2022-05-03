
import pygame 
import json
def startInput():
    pygame.init()
    #waiting for user to plug in controller
    #connecting to controller and initialize
    # xboxcontroller = pygame.joystick.Joystick(0)
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    print(joysticks)
    # xboxcontroller.init()
    #starting loop to obtain x and y controller analog values
    #creating variables to hold x and y value from controller
    left_analog_y_value = 0.0
    right_analog_x_value = 0.0
    while True:
        pygame.event.get()
        #storing analog input from x and y by converting to type float
        # left_analog_y_value = float(format(xboxcontroller.get_axis(1)))
        # right_analog_x_value = float(format(xboxcontroller.get_axis(4)))
        #uploading x and y analog values to network table
        _data = {}
        _data['RightStickXValue'] = right_analog_x_value
        _data['LeftStickYValue']  = left_analog_y_value
        data = data = json.dumps(_data)
        # self.ClientSocket.send(str.encode(data))
        # response = self.ClientSocket.recv(1024) 
        # print(response.decode('utf-8'))
        # print(self.ClientSocket.recv(1024).decode('utf-8'))
        # print("Left Analog Stick: {}\t Right Analog Stick: {}".format(xboxcontroller.get_axis(1),  # left stick y axis
        #                                                     xboxcontroller.get_axis(4)))  # right stick x axis


startInput()