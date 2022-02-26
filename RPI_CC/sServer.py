# Imports
import socket

# Variables
ip_address = '127.0.0.1'
ip_port = 10000
max_connections = 5

txt = 'utf-8'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Code
s.bind((ip_address, ip_port))
s.listen(max_connections)

while True:
    clientsocket, address = s.accept()
    print("{} connected!", address)
    clientsocket.send(b"quit")
