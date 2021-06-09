from threading import Thread
from queue import Queue
import numpy as np


class UserMic(Thread):
    def __init__(self, connection, queue: Queue):
        super().__init__(name='UserMic')
        self.connection = connection
        self.queue: Queue = queue
        self.running = True

    def run(self):
        print(self.name, 'starting...')
        while self.running:
            try:
                self.loop()
            except Exception as e:
                print(self.name, e)

    def loop(self):
        data = self.connection.recv(9000, )
        parsed = np.frombuffer(data, dtype='float32')
        self.queue.put(parsed)
