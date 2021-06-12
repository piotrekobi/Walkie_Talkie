import time
from queue import Full, Empty
from threading import Thread
import numpy as np


class Channel(Thread):
    def __init__(self, data, channel):
        super().__init__(name='Channel')
        self.channel = channel
        self.data = data
        self.running = True

    def run(self):
        print(self.name, 'starting...')
        while self.running:
            try:
                self.loop()
            except Exception as e:
                print(self.name, e)

    def loop(self):
        input_qs, output_qs = self.data.get_queues(self.channel)
        input_arr = []

        for q in input_qs:
            try:
                d = q.get_nowait()
                q.task_done()

                d[2] = int(round(time.time() * 1000))
                input_arr.append(d)
            except Empty:
                input_arr.append(None)


        # input_arr = np.array(input_arr)

        for i, q in enumerate(output_qs):
            for j in range(len(input_arr)):
                if i != j and input_arr[j] is not None:
                    try:
                        input_arr[j][3] = int(round(time.time() * 1000))
                        q.put_nowait(input_arr[j])
                    except Full:
                        pass

    def close(self):
        self.running = False
