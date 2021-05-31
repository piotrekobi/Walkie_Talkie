# Import socket module
import socket
import sounddevice as sd
import soundfile as sf
import numpy as np
import pickle
# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 10000

# connect to the server on local computer
s.connect(('144.126.244.194', port))

# receive data from the server
print(s.recv(17795))
sr = 44100
duration = 0.1
myrecording = sd.rec(int(duration * sr), samplerate=sr, channels=1)
sd.wait()
myrecording = pickle.dumps(myrecording)
print(len(myrecording))
s.send(myrecording)


s.close()
