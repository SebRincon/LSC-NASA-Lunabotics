import time 
import socket
import rospy
from std_msgs.msg import String



class SocketBridge():
    def setup(self):

        serverPort = input("Input Port: ")
        self.HOST = input("Input Host: ")
        if serverPort == 'n':
            self.PORT = 10001
        else: 
            self.PORT = int(serverPort)


    def connect(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectionSuccessful = False
        failedConnection = 0

        while not connectionSuccessful and failedConnection < 5:
            try:
                # Create a client socket
                # Connect to the server
                self.clientSocket.connect((self.address, self.port))
                connectionSuccessful = True
                return True

            except:
                time.sleep(1)
                failedConnection += 1
                pass

        if failedConnection >= 5:
            return False

    def publishData(self, velocity_publisher):
        dataFromServer = self.clientSocket.recv(1024)
        
        velocity_publisher.publish(dataFromServer.decode())

    
if __name__ == '__main__':
    bridge = SocketBridge()
    bridge.setup()
    if bridge.connect():
        rospy.init_node('socket_bridge', anonymous=True)
        velocity_publisher = rospy.Publisher("motor_control/direction", String, queue_size=10)
        while True:
            bridge.publishData(velocity_publisher)
            time.sleep(1)





