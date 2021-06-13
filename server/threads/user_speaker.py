import socket
import time
from threading import Thread
from queue import Queue, Empty

import numpy


class UserSpeaker(Thread):
    def __init__(self, server, connection, queue: Queue, user):
        super().__init__(name='UserSpeaker')
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
                    time.sleep(dt/1000)

        self.user.remove_speaker_queue()

        try:
            self.connection.shutdown(socket.SHUT_WR)
            self.connection.close()
        except OSError:
            pass

        print(self.name, f'ID ({self.user.user_id})', 'stopping...')

    def loop(self):
        try:
            parsed, start, channel_start, channel_end = self.queue.get_nowait()
            self.queue.task_done()
            data = parsed.tobytes()
            # milliseconds = int(round(time.time() * 1000))
            self.connection.send(data)
            # print('dts:', milliseconds - start, milliseconds - channel_start, milliseconds - channel_end)
        except Empty:
            try:
                self.connection.send(numpy.array([1.0e-6, 1.0e-6, 1.0e-6, 1.0e-6], dtype='float32').tobytes())
            except IOError:
                self.running = False
        except IOError:
            self.running = False

    def close(self):
        self.running = False
