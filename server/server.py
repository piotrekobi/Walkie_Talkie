from threads.endpoint_mic import EndpointMic


class Server:
    def __init__(self):
        pass

    def run(self):
        EndpointMic(self, 10000, '').start()

    def add_mic(self, channel, user_id, connection):
        pass

    def add_speaker(self, channel, user_id, connection):
        pass
