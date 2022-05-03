import socket

ClientSocket = socket.socket()
host = '192.168.1.100'
port = 5011

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
while True:
    # Input = input('Say Something: ')
    ClientSocket.send(str.encode('ESP'))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()