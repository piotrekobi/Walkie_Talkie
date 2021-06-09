from threading import Thread

from threads.wrappers.socket_wrapper import SocketWrapper


def parse_token(token):
    text = token.decode('utf-8')
    return text.split('-')


class EndpointGeneric(Thread):
    def __init__(self, data, port, ip, name):
        super().__init__(name=name)
        self.data = data
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

    def loop(self):
        raise NotImplementedError()
