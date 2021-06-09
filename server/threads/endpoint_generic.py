from threading import Thread

from wrappers.socket_wrapper import SocketWrapper


def parse_token(token):
    text = token.decode('utf-8')
    return text.split('_')


class EndpointGeneric(Thread):
    data: any
    socket: SocketWrapper
    running: bool

    def __init__(self, data, port, ip, name):
        super().__init__(name=name)
        self.data = data
        self.socket = SocketWrapper(port, ip)
        self.running = True

    def run(self) -> None:
        self.socket.listen()

        while self.running:
            try:
                self.loop()
            except Exception as e:
                print(e)

    def loop(self):
        raise NotImplementedError()
