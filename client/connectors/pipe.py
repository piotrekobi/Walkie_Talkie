import logging
import sys
from queue import Queue


class ConnectorPipe:
    def __init__(self, *args):
        if len(args) < 2:
            raise IndexError

        self.queues = []

        self.logger = logging.Logger(name='logger')

        self.start_connector = args[0]
        self.middle_connectors = args[1:-1]
        self.end_connector = args[-1]

        queue = Queue()
        self.start_connector.start(queue, self.logger)
        self.queues.append(queue)

        for connector in self.middle_connectors:
            next_queue = Queue()
            self.queues.append(next_queue)
            connector.start(queue, next_queue, self.logger)
            queue = next_queue

        self.end_connector.start(queue, self.logger)

    def close(self):
        self.queues = []

        self.start_connector.close()

        for connector in self.middle_connectors:
            connector.close()

        self.end_connector.close()
