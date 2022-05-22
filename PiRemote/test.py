import socket
import os
import time 
from _thread import *

ServerSocket = socket.socket()
host = '192.168.1.101'
port = 5000
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def thdreaded_client(connection):
    _ping = 'Server Ping'
    connection.send(str.encode('Welcome to the Servern'))
    data = connection.recv(1024)
    log = open('log.txt','a')
    log.write(f'Client Added: {data.decode()}')
    log.close()
    _decoded = data.decode('utf-8')
    if  _decoded == 'GUI':
        while True:
            data = connection.recv(1024)
            f = open('command.txt', 'w')
            f.write(data.decode('utf-8'))
            f.close()
    else: 
        while True:
            try: 
                f = open('command.txt', 'r')
                reply = f.read()
                connection.sendall(str.encode(reply))
                f.close()
            except:
                pass
    connection.close()



def threaded_client(connection):
    connection.send(str.encode('Welcome to the Servern'))
    while True:
        data = connection.recv(2048)
        reply = data.decode('utf-8')
        log = open('log.txt','a')
        log.write(f'\nClient Added: {data.decode()}')
        if not data:
            break

        connection.sendall(str.encode(reply))
        if reply == 'GUI':
            print('GUI Connected')
            while True:
                data = connection.recv(1024)
                print(data.decode())
                f = open('command.txt', 'w')
                f.write(data.decode('utf-8'))
                f.close()
        else: 
            while True:
                time.sleep(0.5)
                try: 
                    f = open('command.txt', 'r')
                    reply = f.read()
                    connection.sendall(str.encode(reply))
                    f.close()
                except:
                    pass

    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
