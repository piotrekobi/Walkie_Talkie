from endpoint_generic import EndpointGeneric, parse_token


class EndpointSpeaker(EndpointGeneric):
    def __init__(self, data, port, ip):
        super().__init__(data, port, ip, 'EndpointSpeaker')

    def loop(self):
        connection = self.socket.accept()

        token = connection.recv(2048)
        channel, user_id = parse_token(token)

        self.data.add_speaker(channel, user_id, connection)

