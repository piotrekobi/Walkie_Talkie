from threads.endpoint_generic import EndpointGeneric, parse_token


class EndpointMic(EndpointGeneric):
    def __init__(self, data, port, ip):
        super().__init__(data, port, ip, 'EndpointMic')

    def loop(self):
        connection = self.socket.accept()

        token = connection.recv(2048)
        channel, user_id = parse_token(token)

        self.data.add_mic(channel, user_id, connection)



