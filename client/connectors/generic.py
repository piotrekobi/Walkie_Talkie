from logging import Logger
from queue import Queue, Empty, Full
from threading import Thread


class ConnectorStartedError(Exception):
    pass


class ConnectorNotStartedError(Exception):
    pass


class GenericConnector:
    queue: Queue
    logger: Logger
    started: bool
    name: str
    thread: Thread

    def __init__(self, name):
        self.name = name
        self.started = False

    def start(self, queue: Queue, logger: Logger):
        if self.started:
            raise ConnectorStartedError()
        self.queue = queue
        self.logger = logger
        self.started = True

        self.thread = Thread(target=self.__start__, name=self.name)
        self.thread.start()

    def __start__(self):
        raise NotImplementedError
    
    def close(self):
        self.started = False


class OutputConnector(GenericConnector):
    def __init__(self, name):
        super().__init__(name)

    def __start__(self):
        self.setup()

        while self.started:
            try:
                self.read_frame(self.queue.get_nowait())
            except Empty:
                pass

        self.exit()

    def setup(self):
        raise NotImplementedError

    def read_frame(self, data):
        raise NotImplementedError

    def exit(self):
        raise NotImplementedError


class InputConnector(GenericConnector):
    def __init__(self, name):
        super().__init__(name)

    def __start__(self):
        self.setup()

        while self.started:
            try:
                self.queue.put_nowait(self.await_frame())
            except Full:
                pass

        self.exit()

    def setup(self):
        raise NotImplementedError

    def await_frame(self):
        raise NotImplementedError

    def exit(self):
        raise NotImplementedError
