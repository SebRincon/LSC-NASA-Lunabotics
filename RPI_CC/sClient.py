# Imports
import socket

# Variables
ip_address = '127.0.0.1'
ip_port = 10000

txt = 'utf-8'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Code
"""Connect to the server"""
s.connect((ip_address, ip_port))

while True:
    msg = s.recv(1024)
    var = msg.decode(txt)
    if var == "quit":
        break

