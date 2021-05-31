# Import socket module 
import socket

# Create a socket object 
s = socket.socket()

# Define the port on which you want to connect 
port = 10000

# connect to the server on local computer 
s.connect(('144.126.244.194', port))

# receive data from the server 
print(s.recv(1024))

s.send(b'dzwek z mikofonu')

# close the connection 
s.close()