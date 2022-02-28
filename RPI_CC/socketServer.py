import socket
import RPi.GPIO as io
import select
import time



class MotorControl():
    def setup(self):
        self.HOST = '10.3.141.1'
        self.PORT = 10001

        ACK_TEXT = 'text_received'

        io.setmode(io.BOARD)
        io.setup(12,io.OUT)
        io.setup(33,io.OUT)

        self.pwmController = io.PWM(12,100)
        self._2pwmController = io.PWM(33,100)

        self.direction = 50
        self.pwmController.start(self.direction)
        self._2pwmController.start(self.direction)

        stop = False

    def setVelocity(self,dutycycle):
        print(dutycycle)
        self.direction = dutycycle
        self.pwmController.ChangeDutyCycle(int(self.direction))
        self._2pwmController.ChangeDutyCycle(int(self.direction))

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
            self.setVelocity(encodedMessage.decode('utf-8'))
            self.sendTextViaSocket(self.direction, conn)

        # end while
    # end function

    
if __name__ == '__main__':
    ctr = MotorControl()
    ctr.setup()
    ctr.connection()
    while True:
        direction = input("Enter Direction: ")
        ctr.setVelocity(direction)