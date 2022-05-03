from rplidar import RPLidar

# Setup the RPLidar
PORT_NAME = 'COM4'
lidar = RPLidar(PORT_NAME)

lidar.stop()
lidar.disconnect()