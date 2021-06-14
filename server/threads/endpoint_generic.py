from threading import Thread

from threads.wrappers.socket_wrapper import SocketWrapper


def parse_token(token):
    try:
        text = token.decode('utf-8')
        fields = text.split('-')

        user_id = fields[1]
        channel_id = fields[0]

        try:
            password = fields[2]
        except IndexError:
            password = None

        return channel_id, user_id

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
