from threads.endpoint_mic import EndpointMic
from threads.endpoint_speaker import EndpointSpeaker
from threads.user_mic import UserMic
from threads.user_speaker import UserSpeaker
from threads.channel import Channel

from queue import Queue
from socket import socket
from threading import Lock


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

        self.channel_lock = Lock()
        self.mic_lock = Lock()
        self.speaker_lock = Lock()

    def set_channel(self, channel):
        with self.channel_lock:
            self.channel = channel

    def set_mic_queue(self, queue, connection):
        with self.mic_lock:
            self.q_mic = queue
            self.c_mic = connection

    def remove_mic_queue(self):
        with self.mic_lock:
            self.c_mic = None
            self.q_mic = None

    def set_speaker_queue(self, queue, connection):
        with self.speaker_lock:
            self.q_speaker = queue
            self.c_speaker = connection

    def remove_speaker_queue(self):
        with self.speaker_lock:
            self.c_speaker = None
            self.q_speaker = None

    def is_ready(self):
        return self.q_mic is not None and self.q_speaker is not None


class UserController:
    def __init__(self):
        self.users = dict()
        self.user_lock = Lock()

    def __call__(self, *args, **kwargs) -> User:
        if len(args) > 0:
            return self.get_instance(args[0])
        else:
            raise KeyError()

    def get_instance(self, user_id: int):
        with self.user_lock:
            try:
                return self.users[user_id]
            except KeyError:
                self.users[user_id] = User(user_id)
                return self.users[user_id]

    def by_channel(self, channel):
        with self.user_lock:
            return [user for user in self.users.values() if user.channel == channel and user.is_ready()]


class Server:
    def __init__(self):
        self.threads = []
        self.get_user = UserController()

        self.channels = dict()

        self.channel_lock = Lock()

    def run(self):
        self.threads.append(EndpointMic(self, 10000, ''))
        self.threads.append(EndpointSpeaker(self, 10001, ''))

        for t in self.threads:
            t.start()

    def stop(self):
        for t in self.threads:
            try:
                t.close()
            except Exception as e:
                print(e)

        for t in self.channels.values():
            try:
                t.close()
            except Exception as e:
                print(e)

    def add_mic(self, channel, user_id, connection):
        q = Queue()

        user = self.get_user(user_id)
        user.set_channel(channel)
        user.set_mic_queue(q, connection)

        if user.is_ready():
            self.start_channel(channel)

        thread = UserMic(self, connection, q, user)
        thread.start()

        self.threads.append(thread)

    def add_speaker(self, channel, user_id, connection):
        q = Queue()

        user = self.get_user(user_id)
        user.set_channel(channel)
        user.set_speaker_queue(q, connection)

        if user.is_ready():
            self.start_channel(channel)

        thread = UserSpeaker(self, connection, q, user)
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

    def start_channel(self, channel):
        with self.channel_lock:
            try:
                self.channels[channel]
            except KeyError:
                self.channels[channel] = Channel(self, channel)
                self.channels[channel].start()
