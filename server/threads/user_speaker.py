from threading import Thread
from queue import Queue


class UserSpeaker(Thread):
    def __init__(self, connection, queue: Queue):
        super().__init__(name='UserSpeaker')
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
        parsed = self.queue.get()
        print(self.name, len(parsed))
        data = parsed.tobytes()
        self.connection.send(data)
