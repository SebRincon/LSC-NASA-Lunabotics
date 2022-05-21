#!/usr/bin/env python3


import threading
from networktables import NetworkTables
import json
import time
import socket

class MotorControl():
    def setup(self):
        # irellivant 
        self.cond = threading.Condition()
        self.notified = [False]
        
        # NetworkTables.initialize(server='10.xx.xx.2')
        NetworkTables.initialize(server='169.254.69.69')
        NetworkTables.addConnectionListener(self.connectionListener, immediateNotify=True)
        self.smart_dashboard = NetworkTables.getTable('SmartDashboard')
        self.datatable = NetworkTables.getTable('datatable')

        # wait for connection 
        with self.cond:
            print("Waiting")
            if not self.notified[0]:
                self.cond.wait()

        # Get table from networktables
        self.motorTable = NetworkTables.getTable('SmartDashboard')

        # Set Default value for testing
        self.motorTable.putNumberArray('velocity',[0,0])
        # Grab values from network table for testing
        _motorFeedback = self.motorTable.getNumberArray(key='velocity', defaultValue=[2.0,2.0])

        # Test Connection
        if _motorFeedback == [0,0]:
            print("Motors Okay")
        else:
            print("Network Table issue")

    # Connection thread 
    def connectionListener(self, connected, info):
        print(info, '; Connected=%s' % connected)
        with self.cond:
            self.notified[0] = True
            self.cond.notify()
    
    def stepperControl(self, conn, pos):
        if pos == 'fr':
            command = self.datatable.getNumber('FrontGearBox',  defaultValue=0)
        elif pos == 'bk':
            command = self.datatable.getNumber('BackGearBox',  defaultValue=0)

        conn.send(command.encode('utf-8'))


    # Start socketServer
    def startSocketServer(self):
        # Set IP and Port for server
        self.HOST = '192.168.1.102'
        self.PORT = 5001

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
        conn, addr = sock.accept()      # Note: execution waits here until the client calls sock.connect()
        print('socket accepted, got connection object')

        # Expect test message 
        _initMsg = conn.recv(1024)

        # Relay test message
        conn.send(_initMsg)

        if _initMsg.decode('utf-8') == 'fr':
            while True:
                self.stepperControl(conn)

        
      

def listener():
    motors = MotorControl()
    motors.setup()
    motors.startSocketServer()
    # motors.startInput()


if __name__ == '__main__':
    listener()


