
import array
import dearpygui.dearpygui as dpg
import numpy as np 
from rplidar import RPLidar
from math import cos, sin, pi, floor


class Viewport():
    def __init__(self):
        self.initSetup = False
        self.initRun = False

    def startLidar(self):
        # Setup the RPLidar
        PORT_NAME = 'COM4'
        self.lidar = RPLidar(PORT_NAME)
        # self.lidar.stop_motor()


        self.scan_data = [0]*360
        self.degrees = np.array(self.scan_data).reshape(4,90)
        self.max_distance = 0
        self.foo = 0
        
        #Creating blank texture for lidar
        self.texture_data = []
        self.texture_grid = np.array([0]*76800).reshape(320, 240)

    def clearLidarErrors(self):
        messageFeed = dpg.get_value('status')
        dpg.set_value('status', f'Cleared Lidar Errors\n{messageFeed}')
        PORT_NAME = 'COM4'
        lidar = RPLidar(PORT_NAME)

        lidar.stop()
        lidar.disconnect()

    
    def getLidarMap(self):
        if not self.initSetup:
            self.startLidar()
            self.initSetup = True
        
        else:
            self.scan_data = [0]*360
            # self.degrees = np.array(self.scan_data).reshape(4,90)
            self.max_distance = 0
            self.foo = 0
            self.texture_data = []
            self.texture_grid = np.array([0]*76800).reshape(320, 240)

        messageFeed = dpg.get_value('status')
        dpg.set_value('status', f'Starting Lidar\n{messageFeed}')
        
        self.foo = 0
        for i, scan in enumerate(self.lidar.iter_scans()):
            for (quality, angle, distance) in scan:
                self.scan_data[min([359, floor(angle)])] = distance
                
                # _angle = min([359, floor(angle)])

                # if _angle >= 0 and angle < 90:    #! Q4
                #     self.scan_data[_angle] = distance
                #     self.degrees[0][_angle] = distance
                
                # elif angle >= 90 and angle < 180: #! Q3
                #     self.scan_data[_angle] = distance
                #     self.degrees[1][_angle - 90 ] = distance
                
                # elif angle >= 180 and angle < 270: #! Q2
                #     self.scan_data[_angle] = distance
                #     self.degrees[2][_angle - 180] = distance
                
                # elif angle >= 270 and angle <360:  #! Q1
                #     self.scan_data[_angle] = distance
                #     self.degrees[3][_angle - 270] = distance

                
            if self.foo < 51:
                self.foo += 1
            if self.foo == 50:
                # print(self.degrees)
                # print(degrees.flatten())
                # print(scan_data)
                self.lidar.stop()
                self.lidar.stop_motor()
                self.lidar.clean_input()
                self.processData()
                break
            


    def processData(self):
        for angle in range(360):
            # if foo == 50:
            #     print(data)
            #     print(len(data))
            
            distance = self.scan_data[angle]
            if distance > 0:                  # ignore initially ungathered data points
                # Updating Max Distance
                self.max_distance = max([min([5000, distance]), self.max_distance])

                # Input data converted from polar coordinates to rectangular coordinates
                radians = angle * pi / 180.0
                
                # r = distance 
                # x = r * cos(angle in rad)
                # y = r * sin(angle in rad)

                x = distance * cos(radians)
                y = distance * sin(radians)

                # point = (160 + int(x / self.max_distance * 119), 120 + int(y / self.max_distance * 119))  # (1,2)
                point = (int(x/self.max_distance * 119), int(y/self.max_distance * 119))  # (1,2)

                if angle < 10:
                    print(point)
                self.texture_grid[point[0]][point[1]] = 1
        _arrayLen = 0
        for i in np.nditer(self.texture_grid):
            if i == 1:
                self.texture_data.append(255 / 255)
                self.texture_data.append(255 / 255)
                self.texture_data.append(255 / 255)
                self.texture_data.append(255 / 255)
                _arrayLen += 1
            else:
                self.texture_data.append(50 / 255)
                self.texture_data.append(50 / 255)
                self.texture_data.append(50 / 255)
                self.texture_data.append(255 / 255)
                _arrayLen += 1

        # while _arrayLen < 76800:
        #     self.texture_data.append(50 / 255)
        #     self.texture_data.append(50 / 255)
        #     self.texture_data.append(50 / 255)
        #     self.texture_data.append(255 / 255)
        #     _arrayLen += 1

        raw_data = array.array('f', self.texture_data)
        dpg.set_value("texture_tag", raw_data)     






class ViewportGUI():
    def createViewport(default_font, VP: Viewport):
            with dpg.child_window(tag='lidarView', width=500, height=450, pos=(205,100), label='Camera Feed'):
                with dpg.group(horizontal=True):
                    dpg.add_button(label='SCAN', callback=VP.getLidarMap)
                    dpg.add_button(label='CLEAR LIDAR ERRORS', callback=VP.clearLidarErrors)
                dpg.bind_font(default_font)
                dpg.add_image("texture_tag", pos=(100,100))