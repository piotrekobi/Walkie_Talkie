# Import socket module
import socket
import threading
import queue
import sys

import numpy as np
import sounddevice as sd

SERVER_IP = '144.126.244.194'

MIC_PORT = 10000
SPEAKER_PORT = 10001

ID = b'999'


def server_output_stream(source_q):
    print('Starting server_output_stream')

    soc = socket.socket()
    soc.connect((SERVER_IP, MIC_PORT))
    soc.send(ID)

    while True:
        try:
            array = source_q.get()
            soc.send(array[0].tobytes())
        except Exception as e:
            print(e)


def server_input_stream(target_q):
    print('Starting server_input_stream')

    soc = socket.socket()
    soc.connect((SERVER_IP, SPEAKER_PORT))
    soc.send(ID)

    while True:
        try:
            recording = soc.recv(100000)
            recording = np.frombuffer(recording, dtype=np.float32)
            target_q.put((recording.copy(), 'ok'))
        except Exception as e:
            print(e)


def sound_output_stream(source_q):
    print('Starting sound_output_stream')

    def callback(out_data, frame_count, time_info, status):
        out_data[:] = source_q.get()

    stream = sd.OutputStream(callback=callback, channels=1, dtype=np.float32)

    with stream:
        while True:
            pass


def sound_input_stream(target_q):
    print('Starting sound_input_stream')

    def callback(in_data, frame_count, time_info, status):
        target_q.put((in_data.copy(), status))

    stream = sd.InputStream(callback=callback, channels=1, dtype=np.float32)

    with stream:
        while True:
            pass


def main():
    try:
        print('Starting...')
        mic = queue.Queue()
        print('Mic queue created...')
        speaker = queue.Queue()
        print('Speaker queue created...')

        threads = [
            threading.Thread(target=sound_input_stream, args=(mic,)),
            threading.Thread(target=server_input_stream, args=(speaker,)),
            threading.Thread(target=sound_output_stream, args=(speaker,)),
            threading.Thread(target=server_output_stream, args=(mic,))
        ]

        for thread in threads:
            thread.start()

        while True:
            pass
    except KeyboardInterrupt:
        for thread in threads:
            thread.ex

        sys.exit('\nInterrupted... Stoping program')


if __name__ == "__main__":
    main()

