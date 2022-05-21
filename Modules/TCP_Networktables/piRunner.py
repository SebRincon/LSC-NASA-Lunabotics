#!/usr/bin/env python3


import threading
from networktables import NetworkTables
import json
import time
import socket
# import socket programming library
import socket
 
# import thread module
from _thread import *
import threading
 
print_lock = threading.Lock()


# ┌─    Remote    ─┐
# │                │
# │                │
# │                │
# └────────────────┘
#          │
#          │
#          │
#          ▼
# ┌──PI4────────────┐
# │ ┌─Socket Server─┴──┐         ┌─Stepper Motor ─┐
# │ │                  │         │                │
# │ │ 192.168.1.102    │◀ ┐   ┌ ▶│                │
# │ │     : 5000       │         │                │
# │ └───────────────┬──┘  │   │  └────────────────┘
# └─────────────────┘
#                         │   │
#                     ┌────────────┐
#                     │ TCP Socket │
#                     └────────────┘
#                         │   │
#  ┌─ RoboRIO ──────┐
#  │ ┌─ Network Tables ┐  │   │
#  │ │                 │
#  │ │  169.254.69.69  │◀ ┴ ─ ┘
#  │ │                 │
#  │ └──────────────┬──┘
#  └────────────────┘
#           │
#           │
#           ▼
#  ┌─  DC Motors   ─┐
#  │                │
#  │                │
#  │                │
#  └────────────────┘


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
        while True:
            if pos == 'fr':
                command = self.datatable.getNumber('FrontGearBox',  defaultValue=0)
            elif pos == 'bk':
                command = self.datatable.getNumber('BackGearBox',  defaultValue=0)
            time.sleep(.2)
            conn.send(command)

    # Start socketServer
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
        conn, addr = sock.accept()      # Note: execution waits here until the client calls sock.connect()
        print('socket accepted, got connection object')


        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Expect test message 
        _initMsg = conn.recv(1024)

        if _initMsg.decode('utf-8') == 'fr':
            conn.send(_initMsg)
            start_new_thread(self.stepperControl, (conn,))


        # Relay test message
        conn.send(_initMsg)
        
        # SAUUUUUCE
    
        # Recive messages and direct them to network tables
        while True:
            # Recive message and decode
            encodedMessage = conn.recv(1024)
            print(encodedMessage.decode('utf-8'))

            # load data into json string
            data = json.loads(encodedMessage.decode('utf-8'))
            

            # pass data string to network table 
            self.datatable.putNumber('RightStickValue', data['RightStickXValue'])
            self.datatable.putNumber('LeftStickValue',  data['LeftStickYValue'])
            self.datatable.putNumber('FrontGearBox',  data['FrontGearBox'])
            self.datatable.putNumber('BackGearBox',  data['BackGearBox'])

            # fetch string from network table
            _rep_right = self.datatable.getNumber('RightStickValue', 0)
            _rep_left = self.datatable.getNumber('LeftStickValue', 0)

            _FrontGearBox = self.datatable.getNumber('FrontGearBox',  0)
            _BacktGearBox = self.datatable.getNumber('BackGearBox',  0)

            _response = f'Joystick Values: {_rep_right} : {_rep_left}\nGearboxes: {_FrontGearBox} : {_BacktGearBox}'
            
            # Print result 
            _response = _response + '\n__success'
            conn.send(_response.encode('utf-8'))
            time.sleep(.2)


def listener():
    motors = MotorControl()
    motors.setup()
    motors.startSocketServer()
    # motors.startInput()


if __name__ == '__main__':
    listener()


