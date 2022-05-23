
import socket
import RPi.GPIO as io
import select
import time
from math import cos, sin, pi, floor
from _thread import *




class MotorControl():
    def setup(self):

        serverPort = input("Input Port: ")
        self.HOST = '192.168.1.100'
        if serverPort == 'n':
            self.PORT = 10001
        else: 
            self.PORT = int(serverPort)

    def setDirection(self, direction:str):
        pass

    def client_thread(self, connection):
        connection.send(encode('Server Ping'))
        data = connection.recv(2048)
        log = open('log.txt','a')
        log.write(f'Client Added: {data.decode()}')
        _decoded = data.decode('utf-8')

        if  _decoded == 'GUI':
            while True:
                data = connection.recv(2048)
                f = open('command.txt', 'w')
                f.write(data.decode('utf-8'))

        else: 
            while True:
                try: 
                    f = open('command.txt', 'r')
                    reply = f.read()
                    connection.sendall(encode(reply))
                except:
                    pass

        connection.close()


    def connection(self):
        # instantiate a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('socket instantiated')
        ThreadCount = 0

        # bind the socket
        sock.bind((self.HOST, self.PORT))
        print('socket binded')

        # start the socket listening
        sock.listen()
        print('socket now listening')

        # accept the socket response from the client, and get the connection object
        conn, addr = sock.accept()      # Note: execution waits here until the client calls sock.connect()
        print('socket accepted, got connection object')
        start_new_thread(self.client_thread, (conn, ))
        
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))

            # self.sendTextViaSocket(self.direction, conn)

        # end while
    # end function

    
if __name__ == '__main__':
    ctr = MotorControl()
    ctr.setup()
    ctr.connection()