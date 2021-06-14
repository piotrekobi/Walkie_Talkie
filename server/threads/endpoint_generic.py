from threading import Thread

import requests
from threads.wrappers.socket_wrapper import SocketWrapper


URL = "http://test-project-domain.com:5000/channels"


def parse_token(token):
    try:
        text = token.decode('utf-8')
        fields = text.split('-')

        user_id = fields[1]
        channel_id = fields[0]
        password = 'None'

        try:
            password = fields[2]
        except IndexError:
            pass

        if requests.get(f"{URL}/{channel_id}/{password}").status_code == 200:
            return channel_id, user_id
        else:
            return None
    except Exception as e:
        print(e)
        return None


class EndpointGeneric(Thread):
    def __init__(self, server, port, ip, name):
        super().__init__(name=name)
        self.server = server
        self.socket = SocketWrapper(port, ip)
        self.running = True

    def run(self) -> None:
        print(self.name, 'starting...')
        self.socket.listen()

        while self.running:
            try:
                self.loop()
            except Exception as e:
                print(self.name, e)

        self.socket.close()
        print(self.name, 'stopping...')

    def loop(self):
        raise NotImplementedError()

    def close(self):
        self.running = False
        self.socket.shutdown()
