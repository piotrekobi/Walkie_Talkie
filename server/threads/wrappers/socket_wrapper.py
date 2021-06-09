import socket


class SocketWrapper:
    soc: socket

    def __init__(self, port, address):
        self.port = port
        self.address = address
        self.enabled = False

    def listen(self):
        if not self.enabled:
            self.soc = socket.socket()
            self.soc.bind((self.address, self.port))
            self.soc.listen(5)
            self.enabled = True
        else:
            raise RuntimeError()

    def accept(self):
        if self.enabled:
            return self.soc.accept()[0]
        else:
            raise RuntimeError()
