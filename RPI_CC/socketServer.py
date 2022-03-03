
import socket
import RPi.GPIO as io
import select
import time
from math import cos, sin, pi, floor
import pygame
from rplidar import RPLidar, RPLidarException




class MotorControl():
    def setup(self):

        serverPort = input("Input Port: ")
        self.HOST = '10.3.141.1'
        if serverPort == 'n':
            self.PORT = 10001
        else: 
            self.PORT = int(serverPort)


        ACK_TEXT = 'text_received'

        io.setmode(io.BOARD)
        io.setup(12,io.OUT)
        io.setup(33,io.OUT)
        io.setup(32,io.OUT)
        io.setup(35,io.OUT)

        self.frontRightMotor = io.PWM(12,100)
        self.fronLeftMotor = io.PWM(33,100)
        self.backRightMotor = io.PWM(32,100)
        self.backLeftMotor = io.PWM(35,100)

        self.direction = 50

        self.frontRightMotor.start(self.direction)
        self.fronLeftMotor.start(self.direction)
        self.backRightMotor.start(self.direction)
        self.backLeftMotor.start(self.direction)
        

        stop = False

    def startLidar(self):
        pygame.init()
        self.lcd = pygame.display.set_mode((320,240))
        pygame.mouse.set_visible(False)
        self.lcd.fill((0,0,0))
        pygame.display.update()
        PORT_NAME = '/dev/ttyUSB0'
        self.lidar = RPLidar(PORT_NAME)

    def startLidarStream(self):
        self.lidarHost = '10.3.141.1'
        inputPort = input('Choose a Port: ')
        if inputPort == 'n':
            self.lidarPort = 20002
        else:
            self.lidarPort = int(inputPort)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('socket instantiated')

        # bind the socket
        sock.bind((self.lidarHost, self.lidarPort))
        print('socket binded')

        # start the socket listening
        sock.listen()
        print('socket now listening')

        # accept the socket response from the client, and get the connection object
        conn, addr = sock.accept()      # Note: execution waits here until the client calls sock.connect()
        print('socket accepted, got connection object')

        scan_data = [0]*360
        max_distance = 0 
        try:
            for i, scan in enumerate(self.lidar.iter_scans()):
                for (_, angle, distance) in scan:
                    scan_data[min([359, floor(angle)])] = distance

                self.lcd.fill((0,0,0))
                for angle in range(360):
                    distance = scan_data[angle]

                    if distance > 0:                  # ignore initially ungathered data points
                        max_distance = max([min([5000, distance]), max_distance])
                        radians = angle * pi / 180.0
                        x = distance * cos(radians)
                        y = distance * sin(radians)
                        point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))
                        message= (f"{point[0]} - {point[1]} ")
                        conn.sendall(message.encode())
                        
                        feedback = conn.recv(1024)

                        self.lcd.set_at(point, pygame.Color(255, 255, 255))
                pygame.display.update()
        except RPLidarException:
            self.lidar.stop()
            self.lidar.disconnect()


    def setVelocity(self,dutycycle):
        print(dutycycle)
        self.direction = dutycycle

        self.frontRightMotor.ChangeDutyCycle(int(self.direction))
        self.fronLeftMotor.ChangeDutyCycle(int(self.direction))
        self.backRightMotor.ChangeDutyCycle(int(self.direction))
        self.backLeftMotor.ChangeDutyCycle(int(self.direction))

    def setDirection(self, genDirection:str):
        directions = {'forward': [4,24,4,24], 'backward': [24, 4, 24, 4],'stop': [0,0,0,0]}

        if genDirection == 'forward':
            self.frontRightMotor.ChangeDutyCycle(directions['forward'][0])
            self.fronLeftMotor.ChangeDutyCycle(directions['forward'][1])
            self.backRightMotor.ChangeDutyCycle(directions['forward'][2])
            self.backLeftMotor.ChangeDutyCycle(directions['forward'][3])

        elif  genDirection == 'forward':
            self.frontRightMotor.ChangeDutyCycle(directions['backward'][0])
            self.fronLeftMotor.ChangeDutyCycle(directions['backward'][1])
            self.backRightMotor.ChangeDutyCycle(directions['backward'][2])
            self.backLeftMotor.ChangeDutyCycle(directions['backward'][3])

        elif  genDirection == 'stop':
            self.frontRightMotor.ChangeDutyCycle(directions['stop'][0])
            self.fronLeftMotor.ChangeDutyCycle(directions['stop'][1])
            self.backRightMotor.ChangeDutyCycle(directions['stop'][2])
            self.backLeftMotor.ChangeDutyCycle(directions['stop'][3])


    def sendTextViaSocket(self, message, sock):
        # encode the text message
        encodedMessage = bytes(message, 'utf-8')

        # send the data vi the socket to the server
        sock.sendall(encodedMessage)

        # receive acknowledgment from the server
        #encodedAckText = sock.recv(1024)
        #ackText = encodedAckText.decode('utf-8')

        # log if acknowledgment was successful
        # end if
    # end function


    def connection(self):
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

        myCounter = 0
        while True:
            encodedMessage = conn.recv(1024)
            print(encodedMessage.decode('utf-8'))
            self.setDirection(encodedMessage.decode('utf-8'))
            # self.sendTextViaSocket(self.direction, conn)

        # end while
    # end function

    
if __name__ == '__main__':
    ctr = MotorControl()
    ctr.setup()
    #ctr.startLidar()
    #ctr.startLidarStream()
    ctr.connection()
    #while True:
    #    direction = input("Enter Direction: ")
    #    ctr.setVelocity(direction)
