# Import socket module
import socket
import sounddevice as sd
import soundfile as sf
import numpy as np
import pickle
import threading


# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 10000

# connect to the server on local computer
s.connect(('144.126.244.194', port))


def receive(soc):
    while True:
        recording = soc.recv(18000)
        recording = pickle.loads(recording)
        sr = 44100
        sd.play(recording, sr, channels=1)
        sd.wait()


def send(soc):
    while True:
        sr = 44100
        duration = 0.1
        recording = sd.rec(int(duration * sr), samplerate=sr, channels=1)
        sd.wait()
        recording = pickle.dumps(recording)
        soc.send(recording)


threading.Thread(target=receive, args=(s,)).start()
threading.Thread(target=send, args=(s,)).start()

# receive data from the server
#print(s.recv(17795))
#sr = 44100
#duration = 0.1
#myrecording = sd.rec(int(duration * sr), samplerate=sr, channels=1)
#sd.wait()
#myrecording = pickle.dumps(myrecording)
#print(len(myrecording))
#s.send(myrecording)


try:
    while True:
        pass
except KeyboardInterrupt:
    s.close()
