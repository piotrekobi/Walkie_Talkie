from threading import Thread
from queue import Queue
import numpy as np


class Channel(Thread):
    def __init__(self, data, channel):
        super().__init__(name='Channel')
        self.channel = channel
        self.data = data

    def run(self):
        while self.running:
            try:
                self.loop()
            except Exception as e:
                print(e)

    def loop(self):
        input_qs, output_qs = self.data.get_queues(self.channel)

        input_arr = []

        for q in input_qs:
            input_arr.append(q.get())

        for i, q in enumerate(output_qs):
            q.put(np.sum(input_arr[:i] + input_arr[i:]))
