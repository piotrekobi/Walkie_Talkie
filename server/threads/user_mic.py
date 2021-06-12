from threading import Thread
from queue import Queue, Full
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
        try:
            data = self.connection.recv(8192)
            parsed = np.frombuffer(data, dtype='float32')
            # zeros = np.zeros(2048)
            # zeros[:parsed.shape[0]] = parsed
            self.queue.put_nowait(parsed)
        except Full:
            pass

    def close(self):
        self.running = False
