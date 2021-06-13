from threading import Thread

from threads.wrappers.socket_wrapper import SocketWrapper


def parse_token(token):
    text = token.decode('utf-8')
    return text.split('-')


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
