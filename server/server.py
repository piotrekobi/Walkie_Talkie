from threads.endpoint_mic import EndpointMic
from threads.endpoint_speaker import EndpointSpeaker
from threads.user_mic import UserMic
from threads.user_speaker import UserSpeaker

from queue import Queue
from socket import socket


class User:
    q_mic: Queue
    q_speaker: Queue
    c_mic: socket
    c_speaker: socket
    channel: int

    def __init__(self, user_id):
        self.user_id = user_id
        self.c_mic = None
        self.c_speaker = None
        self.q_mic = None
        self.q_speaker = None
        self.channel = None

    def set_channel(self, channel):
        self.channel = channel

    def set_mic_queue(self, queue, connection):
        self.q_mic = queue
        self.c_mic = connection

    def set_speaker_queue(self, queue, connection):
        self.q_speaker = queue
        self.c_speaker = connection

    def is_ready(self):
        return self.q_mic is not None and self.q_speaker is not None and self.channel is not None


class UserController:
    def __init__(self):
        self.users = dict()

    def __call__(self, *args, **kwargs) -> User:
        if len(args) > 0:
            self.get_instance(args[0])
        else:
            raise KeyError()

    def get_instance(self, user_id: int):
        try:
            print(self.users[user_id])
            return self.users[user_id]
        except KeyError:
            self.users[user_id] = User(user_id)
            print(self.users[user_id])
            return self.users[user_id]

    def by_channel(self, channel):
        return [user for user in self.users.items() if user.channel == channel and user.is_ready()]


class Server:
    def __init__(self):
        self.threads = []
        self.get_user = UserController()

    def run(self):
        self.threads.append(EndpointMic(self, 10000, ''))
        self.threads.append(EndpointSpeaker(self, 10001, ''))

        for t in self.threads:
            t.start()

    def stop(self):
        for t in self.threads:
            try:
                t.running = False
            except Exception as e:
                print(e)

    def add_mic(self, channel, user_id, connection):
        q = Queue()

        user = self.get_user(user_id)
        user.set_channel(channel)
        user.set_mic_queue(q, connection)

        thread = UserMic(connection, q)
        thread.start()

        self.threads.append(thread)

    def add_speaker(self, channel, user_id, connection):
        q = Queue()

        user = self.get_user(user_id)
        user.set_channel(channel)
        user.set_mic_queue(q, connection)

        thread = UserSpeaker(connection, q)
        thread.start()

        self.threads.append(thread)

    def get_queues(self, channel):
        users = self.get_user.by_channel(channel)

        input_qs = [0 for _ in range(len(users))]
        output_qs = [0 for _ in range(len(users))]

        for i, user in enumerate(users):
            input_qs[i] = user.q_mic
            output_qs[i] = user.q_speaker

        return input_qs, output_qs
