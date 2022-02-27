import socket 

HOST = '10.3.141.105' # Server IP or Hostname
#HOST = '127.0.0.1' # Server IP or Hostname
#HOST = 'raspberrypi.local'# Server IP or Hostname
PORT = 10001 # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

#managing error exception
try:
    s.bind((HOST, PORT))
except socket.error:
    print("Bind failed")
s.listen(5)
print('Socket awaiting messages')
(conn, addr) = s.accept()
print('Connected')

# awaiting for message
while True:
    data = conn.recv(1024)
    data = data.decode()
    print('I sent a message back in response to: ' + data)
    reply = ''

     # process your message
    if data == 'Hello':
        reply = 'Hi, back!'
    elif data == 'This is important':
        reply = 'OK, I have done the important thing you have asked me!'

        #and so on and on until...
    elif data == 'quit':
        conn.send('Terminating')
        break
    else:
        repl = 'Unknown command'

        # Sending reply
        reply = reply.encode()
        conn.send(reply)
conn.close() # Close connections
