#! /usr/bin/env python3
import rospy
import socket
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class gearboxMiddle():

    def startSocketServer(self):
        # Set IP and Port for server
        self.HOST = '192.168.1.102'
        self.PORT = 5000

        # instantiate a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('socket instantiated')

        # bind the socket
        sock.bind((self.HOST, self.PORT))
        print('socket binded')

        # start the socket listening
        sock.listen()
        print('socket now listening')

        # accept the socket response from the client, and get the connection object
        self.conn, addr = sock.accept()      # Note: execution waits here until the client calls sock.connect()
        print('socket accepted, got connection object')

        # Expect test message 
        _initMsg = self.conn.recv(1024)

        # Relay test message
        self.conn.send(_initMsg)


    def sendControl(self, message):
        self.conn.send(message.encode('utf-8'))

    def listener(self):
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber('gearbox', String, self.sendControl)


if __name__ == "__main__":

    motorsControl = gearboxMiddle()
    motorsControl.startSocketServer()
    motorsControl.listener()