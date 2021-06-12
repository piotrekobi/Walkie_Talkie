from threading import Thread
from queue import Queue, Empty


class UserSpeaker(Thread):
    def __init__(self, connection, queue: Queue, user):
        super().__init__(name='UserSpeaker')
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
            parsed = self.queue.get_nowait()
            self.queue.task_done()
            data = parsed.tobytes()
            self.connection.send(data)
        except Empty:
            pass

    def close(self):
        self.running = False
