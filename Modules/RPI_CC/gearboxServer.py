
import socket
import RPi.GPIO as io
import select
import time
from math import cos, sin, pi, floor

 
# import thread module
from _thread import *
import threading
 
print_lock = threading.Lock()



class GearboxController():
    def setup(self):
        self.HOST = '192.168.1.101'
        self.PORT = 5001
        stop = False
    
    def client_thread(self, connection):
        connection.send(str.encode('Server Ping'))
        data = connection.recv(2048)
        log = open('log.txt','a')
        log.write(f'Client Added: {data.decode()}')
        _decoded = data.decode('utf-8')
        connection.send(data)

        if  _decoded == 'GUI':
            print('GUI CONNECTED')
            while True:
                time.sleep(.5)
                data = connection.recv(2048)
                f = open('command.txt', 'w')
                f.write(data.decode('utf-8'))
                print(data.decode('utf-8'))
                f.close()

        elif _decoded == 'fr': 
            print('Front Motor CONNECTED')
            while True:
                try: 
                    time.sleep(.5)
                    f = open('command.txt', 'r')
                    reply = f.read()
                    connection.sendall(str.encode(reply))
                    f.close()
                except:
                    pass

        elif _decoded == 'bk': 
            print('Back Motor CONNECTED')
            while True:
                try: 
                    time.sleep(.5)
                    f = open('command.txt', 'r')
                    reply = f.read()
                    connection.sendall(str.encode(reply))
                    f.close()
                except:
                    pass

        connection.close()

    def connection(self):
        ThreadCount = 0

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
        while True:
            conn, addr = sock.accept()      # Note: execution waits here until the client calls sock.connect()
            print('socket accepted, got connection object')
            start_new_thread(self.client_thread, (conn, ))
            
            ThreadCount += 1
            print('Thread Number: ' + str(ThreadCount))



        # end while
    # end function

    
if __name__ == '__main__':
    ctr = GearboxController()
    ctr.setup()
    ctr.connection()
