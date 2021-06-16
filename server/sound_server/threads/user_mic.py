import socket
from threading import Thread
from queue import Queue, Full
import numpy as np
import time


class UserMic(Thread):
    def __init__(self, server, connection, queue: Queue, user):
        super().__init__(name='UserMic')
        self.server = server
        self.connection = connection
        self.user = user
        self.queue: Queue = queue
        self.running = True

    def run(self):
        print(self.name, f'ID ({self.user.user_id})', 'starting...')

        while self.running:
            start_time = int(round(time.time() * 1000))
            try:
                self.loop()
            except Exception as e:
                print(self.name, e)
            finally:
                end_time = int(round(time.time() * 1000))
                dt = 40 - (end_time - start_time)
                if dt > 0:
                    time.sleep(dt / 1000)

        self.user.remove_mic_queue()
        self.connection.shutdown(socket.SHUT_WR)
        self.connection.close()
        print(self.name, f'ID ({self.user.user_id})', 'stopping...')

    def loop(self):
        try:
            data = self.connection.recv(8192)
            if data == b'$close$':
                raise ValueError
            parsed = np.frombuffer(data, dtype='float32')
            self.queue.put_nowait(parsed)
        except Full:
            pass
        except ValueError:
            self.running = False

    def close(self):
        self.running = False
