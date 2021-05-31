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
        try:
            recording = soc.recv(18000)
            print(f'received: {len(recording)}')
            recording = pickle.loads(recording)
            sr = 44100
            sd.playrec(recording, sr, channels=1)
            sd.wait()
        except Exception as e:
            print(e)


def send(soc):
    while True:
        try:
            sr = 44100
            duration = 0.05
            recording = sd.rec(int(duration * sr), samplerate=sr, channels=1)
            sd.wait()
            recording = pickle.dumps(recording)
            print(f'packed: {len(recording)}')
            soc.send(recording)
        except Exception as e:
            print(e)


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
