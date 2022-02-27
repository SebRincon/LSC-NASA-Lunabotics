

import socket

HOST = '10.3.141.1' # Enter IP or Hostname of your server
PORT = 10001 # Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#Lets loop awaiting for your input
while True:
    command = input('Enter your command: ')
    s.send(command.encode())
    reply = s.recv(1024)
    reply = reply.decode()
    if reply == 'Terminate':
        break
    print(reply)


