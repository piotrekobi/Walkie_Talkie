import time
from queue import Full, Empty
from threading import Thread
import numpy as np


class Channel(Thread):
    def __init__(self, server, channel):
        super().__init__(name='Channel')
        self.channel = channel
        self.server = server
        self.running = True

    def run(self):
        print(self.name, f'ID ({self.channel})', 'starting...')

        while self.running:
            start_time = int(round(time.time() * 1000))
            try:
                self.loop()
            except Exception as e:
                print(self.name, e)
            finally:
                end_time = int(round(time.time() * 1000))
                dt = 30 - (end_time - start_time)
                if dt > 0:
                    time.sleep(dt / 1000)

        print(self.name, f'ID ({self.channel})', 'stopping...')

    def loop(self):
        input_qs, output_qs = self.server.get_queues(self.channel)

        # if len(input_qs) == 0:
        #     self.running = False
        #     return

        input_arr = []

        for q in input_qs:
            try:
                d = q.get_nowait()
                q.task_done()

                d[2] = int(round(time.time() * 1000))
                input_arr.append(d)
            except Empty:
                input_arr.append(None)

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
