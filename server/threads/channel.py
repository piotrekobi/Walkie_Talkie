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
            input_arr.append(q.get())

        # input_arr = np.array(input_arr)

        for i, q in enumerate(output_qs):
            for j in range(len(input_arr)):
                if i != j:
                    q.put(input_arr[j])

    def close(self):
        self.running = False
