# SPDX-FileCopyrightText: 2019 Dave Astels for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Consume LIDAR measurement file and create an image for display.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""

import os
from math import cos, sin, pi, floor
import pygame
from rplidar import RPLidar

# Set up pygame and the display
pygame.init()
lcd = pygame.display.set_mode((320,240))
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))
pygame.display.update()

# Setup the RPLidar
PORT_NAME = 'COM4'
lidar = RPLidar(PORT_NAME)
lidar.stop_motor()
input('Go?: ')
# used to scale data to fit on the screen
max_distance = 0

#pylint: disable=redefined-outer-name,global-statement

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
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))  # (1,2) 
            lcd.set_at(point, pygame.Color(255, 255, 255))
    pygame.display.update()


scan_data = [0]*360

try:
    for i, scan in enumerate(lidar.iter_scans()):
        for (quality, angle, distance) in scan:
            
            scan_data[min([359, floor(angle)])] = distance
                # if foo == 50:
                #     print(f'Quality: {quality}')
                #     print(f'Angle: {angle}')
                #     print(f'Distance: {distance}')
        foo += 1
        process_data(scan_data,foo)

except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()