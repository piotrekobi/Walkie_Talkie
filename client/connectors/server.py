from connectors.generic import OutputConnector, InputConnector

import socket
import numpy as np


class ServerConnector:
    url: str
    port: int
    connection_id: str
    soc: socket.socket

    def __init__(self):
        raise NotImplementedError

    def setup_server(self):
        self.logger.log(1, 'Starting Thread')
        self.soc = socket.socket()

        self.logger.log(1, f'Connecting to socket at {self.url}:{self.port}')
        self.soc.connect((self.url, self.port))

        self.logger.log(1, f'Connected to {self.url}:{self.port}. Sending connection ID')
        self.soc.send(self.connection_id.encode('utf-8'))

        self.logger.log(1, f'Connection ID set to {self.connection_id} for {self.url}:{self.port}')

    def destroy_server(self):
        self.logger.log(1, 'Stoping Thread')
        self.soc.close()


class ServerSoundOutputConnector(OutputConnector, ServerConnector):
    def __init__(self, url: str, port: int, connection_id: str):
        self.url = url
        self.port = port
        self.connection_id = connection_id

        super().__init__()

    def setup(self):
        self.setup_server()

    def read_frame(self, data):
        try:
            self.soc.send(data.tobytes())
        except Exception as e:
            self.logger.error(e)

    def destroy(self):
        self.destroy_server()


class ServerSoundInputConnector(InputConnector, ServerConnector):
    def __init__(self, url: str, port: int, connection_id: str):
        self.url = url
        self.port = port
        self.connection_id = connection_id

        super().__init__()

    def setup(self):
        self.setup_server()

    def await_frame(self):
        try:
            recording = np.frombuffer(self.soc.recv(8192), dtype='float32')
            return recording
        except Exception as e:
            self.logger.error(e)

    def destroy(self):
        self.destroy_server()
