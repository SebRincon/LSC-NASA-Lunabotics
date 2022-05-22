
import socket
import RPi.GPIO as io
import select
import time
from math import cos, sin, pi, floor




class MotorControl():
    def setup(self):

        serverPort = input("Input Port: ")
        self.HOST = '192.168.1.100'
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

    def setVelocity(self,dutycycle):
        print(dutycycle)
        self.direction = dutycycle

        self.frontRightMotor.ChangeDutyCycle(int(self.direction))
        self.fronLeftMotor.ChangeDutyCycle(int(self.direction))
        self.backRightMotor.ChangeDutyCycle(int(self.direction))
        self.backLeftMotor.ChangeDutyCycle(int(self.direction))

    def setDirection(self, genDirection:str):
        directions = {
            'f': [4,24,4,24],
            'b': [24, 4, 24, 4],
            's': [0,0,0,0],
            'fl': [0,0,0,0],
            'fr': [0,0,0,0],
            'br': [0,0,0,0],
            'bl': [0,0,0,0],
            'r': [0,0,0,0],
            'l': [0,0,0,0],
            }

        
        self.frontRightMotor.ChangeDutyCycle(directions[genDirection][0])
        self.fronLeftMotor.ChangeDutyCycle(directions[genDirection][1])
        self.backRightMotor.ChangeDutyCycle(directions[genDirection][2])
        self.backLeftMotor.ChangeDutyCycle(directions[genDirection][3])


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
