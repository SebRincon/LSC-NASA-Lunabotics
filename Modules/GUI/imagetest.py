from PIL import Image
from rplidar import RPLidar
from math import cos, sin, pi, floor
import numpy as np


PORT_NAME = '/dev/ttyUSB0'                                                             
# PORT_NAME = 'COM4'                                                                   
lidar = RPLidar(PORT_NAME)                                                        
# lidar.stop_motor()                                                              
                                                                                       
                                                                                       
scan_data = [0]*360                                                                                            
max_distance = 0                                                                  
foo = 0                                                                           
                                                                                       
#Creating blank texture for lidar                                                      
texture_data = []                                                                 
texture_grid = np.array([0]*76800).reshape(320, 240)  

w, h = 400, 400
data = np.zeros((w, h, 3), dtype=np.uint8)
data[0:50, 0:50] = [255, 0, 0] # red patch in upper left
img = Image.fromarray(data, 'RGB')
img.save('my.png')
img.show()
