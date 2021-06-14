from threads.endpoint_generic import EndpointGeneric, parse_token


class EndpointMic(EndpointGeneric):
    def __init__(self, server, port, ip):
        super().__init__(server, port, ip, 'EndpointMic')

    def loop(self):
        connection, address = self.socket.accept()

        token = connection.recv(2048)

        try:
            channel, user_id = parse_token(token)

            print(self.name, f'connecting mic from {address} to channel {channel} with ID {user_id}')
            self.server.add_mic(channel, user_id, connection)
        except Exception:
            connection.close()



