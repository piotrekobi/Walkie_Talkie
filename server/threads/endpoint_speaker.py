from threads.endpoint_generic import EndpointGeneric, parse_token


class EndpointSpeaker(EndpointGeneric):
    def __init__(self, server, port, ip):
        super().__init__(server, port, ip, 'EndpointSpeaker')

    def loop(self):
        connection, address = self.socket.accept()

        token = connection.recv(2048)

        try:
            channel, user_id = parse_token(token)

            print(self.name, f'connecting speaker from {address} to channel {channel} with ID {user_id}')
            self.server.add_speaker(channel, user_id, connection)
        except Exception:
            print(self.name, f'connecting failed! From {address} to channel {channel} with ID {user_id}')
            connection.close()

