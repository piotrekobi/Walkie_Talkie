# Import socket module
import socket
import threading
import queue
import sys

import numpy as np
import sounddevice as sd

FRAMESIZE = 256
SAMPLERATE = 44100

SERVER_IP = '144.126.244.194'

MIC_PORT = 10000
SPEAKER_PORT = 10001

ID = b'999'


def server_output_stream(source_q):
    print('Starting server_output_stream')

    soc = socket.socket()
    print('Connecting to MIC_SOCKET...')
    soc.connect((SERVER_IP, MIC_PORT))
    print('Connected to MIC_SOCKET. Sending ID...')
    soc.send(ID)
    print('ID set for MIC_SOCKET')

    while True:
        try:
            array = source_q.get()
            #print(f'server_output_stream: Read from queue: {len(array)}')
            soc.send(array[0].tobytes())
        except Exception as e:
            print(e)


def server_input_stream(target_q):
    print('Starting server_input_stream')

    soc = socket.socket()
    print('connecting to SPEAKER_SOCKET...')
    soc.connect((SERVER_IP, SPEAKER_PORT))
    print('Connected to SPEAKER_SOCKET. Sending ID...')
    soc.send(ID)
    print('ID set for SPEAKER_SOCKET')

    while True:
        try:
            recording = soc.recv(100000)
            recording = np.frombuffer(recording, dtype=np.float32)
            #print(f'server_input_stream: Written to queue: {len(recording)}')
            target_q.put((recording.copy(), 'ok'))
        except Exception as e:
            print(e)


def sound_output_stream(source_q):
    print('Starting sound_output_stream')

    stream = sd.OutputStream(channels=1, dtype=np.float32, blocksize=FRAMESIZE, samplerate=SAMPLERATE)

    with stream:
        while True:
            data = source_q.get()[0]
            stream.write(data)


def sound_input_stream(target_q):
    print('Starting sound_input_stream')

    stream = sd.InputStream(channels=1, dtype=np.float32, blocksize=FRAMESIZE, samplerate=SAMPLERATE)

    with stream:
        while True:
            data = stream.read(FRAMESIZE)[0]
            target_q.put((data, 'ok'))


def main():
    try:
        print('Starting...')
        mic = queue.Queue(maxsize=1000)
        print('Mic queue created...')
        speaker = queue.Queue(maxsize=1000)
        print('Speaker queue created...')

        threads = [
            threading.Thread(target=sound_input_stream, args=(mic,), name='sound_input_stream'),
            threading.Thread(target=server_input_stream, args=(speaker,), name='server_input_stream'),
            threading.Thread(target=sound_output_stream, args=(speaker,), name='sound_output_stream'),
            threading.Thread(target=server_output_stream, args=(mic,), name='server_output_stream')
        ]

        for thread in threads:
            thread.start()

        while True:
            pass
    except KeyboardInterrupt:

        sys.exit('\nInterrupted... Stoping program')


if __name__ == "__main__":
    main()

