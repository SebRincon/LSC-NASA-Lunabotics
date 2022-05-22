
import socket
import RPi.GPIO as io
import select
import time
from math import cos, sin, pi, floor

class MotorControl():
    def setup(self):

        self.HOST = '192.168.1.101'
        self.PORT = 5000

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


    def setVelocity(self, velCommand ):
    
        self.frontRightMotor.ChangeDutyCycle(velCommand[0])
        self.fronLeftMotor.ChangeDutyCycle(velCommand[1])
        self.backRightMotor.ChangeDutyCycle(velCommand[2])
        self.backLeftMotor.ChangeDutyCycle(velCommand[3])

    def setDirection(self, genDirection:str):
        directions = {
            # fr_right - fr_left - bk_right - bk_left 
            'forward': [4,24,4,24],
            'backward': [24, 4, 24, 4],
            'stop': [0,0,0,0],
            'fr_left': [4,4,4,4],
            'fr_right': [24,24,24,24],
            'bk_left': [24,24,24,24],
            'bk_left': [4,4,4,4],

            }

        self.setVelocity(directions[genDirection])

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
