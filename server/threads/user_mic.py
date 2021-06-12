from threading import Thread
from queue import Queue
import numpy as np


class UserMic(Thread):
    def __init__(self, connection, queue: Queue, user):
        super().__init__(name='UserMic')
        self.connection = connection
        self.user = user
        self.queue: Queue = queue
        self.running = True

    def run(self):
        print(self.name, 'starting...')
        print(self.name, id(self.queue), self.user.user_id)
        while self.running:
            try:
                self.loop()
            except Exception as e:
                print(self.name, e)

    def loop(self):
        data = self.connection.recv(9000)
        parsed = np.frombuffer(data, dtype='float32')
        zeros = np.zeros((2048,))
        zeros[:parsed.shape[0]] = parsed

        self.queue.put(zeros)

    def close(self):
        self.running = False
