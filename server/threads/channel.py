from threading import Thread
from queue import Queue
import numpy as np


class UserMic(Thread):
    def __init__(self, channel, queues: list[(Queue, Queue)]):
        super().__init__(name='UserMic')
        self.channel = channel
        self.queues = queues

    def run(self):
        while self.running:
            try:
                self.loop()
            except Exception as e:
                print(e)

    def loop(self):
        data = self.connection.recv(9000)
        parsed = np.frombuffer(data, dtype='float32')
        self.queue.put(parsed)
