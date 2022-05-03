import numpy as np 
import pygame
from rplidar import RPLidar
from math import cos, sin, pi, floor

# Set up pygame and the display
pygame.init()
lcd = pygame.display.set_mode((320,240))
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))
pygame.display.update()

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)
lidar.stop_motor()
# input('Go?: ')
scan_data = [0]*360


degrees = np.array(scan_data).reshape(4,90)
max_distance = 0
foo = 0

def process_data(data,foo):
    global max_distance
    lcd.fill((0,0,0))
    
    
    for angle in range(360):
        # if foo == 50:
        #     print(data)
        #     print(len(data))
        
        distance = data[angle]
        if distance > 0:                  # ignore initially ungathered data points
            # Updating Max Distance
            max_distance = max([min([5000, distance]), max_distance])

            # Input data converted from polar coordinates to rectangular coordinates
            radians = angle * pi / 180.0
            
            # r = distance 
            # x = r * cos(angle in rad)
            # y = r * sin(angle in rad)

            x = distance * cos(radians)
            y = distance * sin(radians)

            point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))  # (1,2) 
            lcd.set_at(point, pygame.Color(255, 255, 255))
    pygame.display.update()



try:
    for i, scan in enumerate(lidar.iter_scans()):
        for (quality, angle, distance) in scan:
            _angle = min([359, floor(angle)])
            if _angle >= 0 and angle < 90:    #! Q4
                scan_data[_angle] = distance
                # degrees[0][min([359, floor(angle)])] = distance
            
            elif angle >= 90 and angle < 180: #! Q3
                scan_data[_angle] = distance
                # degrees[1][min([359, floor(angle) - 90 ])] = distance
            
            elif angle >= 180 and angle < 270: #! Q2
                scan_data[min([359, floor(angle)])] = distance
                # degrees[2][min([359, floor(angle) - 180])] = distance
            
            elif angle >= 270 and angle <360:  #! Q1
                scan_data[min([359, floor(angle)])] = distance
                # degrees[3][min([359, floor(angle) - 270])] = distance

                
                # if foo == 50:
                #     print(f'Quality: {quality}')
                #     print(f'Angle: {angle}')
                #     print(f'Distance: {distance}')
        # if foo < 51:
        #     foo += 1
        # if foo == 50:
        #     print(degrees)
            # print(degrees.flatten())
            # print(scan_data)
        process_data(scan_data,foo)


except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.stop_motor()
lidar.disconnect()