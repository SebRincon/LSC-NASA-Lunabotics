
import array
from pickletools import uint8
import dearpygui.dearpygui as dpg
import numpy as np 
# from rplidar import RPLidar
from math import cos, sin, pi, floor
# from PIL import Image
# import pygame



class Viewport():
    def __init__(self):
        self.initSetup = False
        self.initRun = False
        
class ViewportGUI():
    def createViewport(default_font, VP: Viewport):
            with dpg.child_window(tag='lidarView', width=500, height=450, pos=(205,100), label='Camera Feed'):
                # with dpg.group(horizontal=True):
                    # dpg.add_button(label='SCAN', callback=VP.getLidarMap)
                    # dpg.add_button(label='CLEAR LIDAR ERRORS', callback=VP.clearLidarErrors)
                dpg.bind_font(default_font)
                dpg.add_image("texture_tag")
