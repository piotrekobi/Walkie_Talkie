import socket
import threading
import queue





class SocketSoundServer:
    def __init__(self, port_in, port_out, address):
        self.connections = dict()
        self.socket_in = SocketWrapper(port_in, address)
        self.socket_out = SocketWrapper(port_out, address)

    def start(self):
        self.socket_in.listen()

        self.socket_out.listen()

        threading.Thread(target=self.run_server_in).start()
        threading.Thread(target=self.run_server_out).start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.close()

    def close(self):
        for connection in self.connections:
            try:
                connection.close()
            except Exception:
                pass

        self.socket.close()

    def run_client(self, user_id, current_connection):
        while True:
            data = current_connection.recv(9000)
            for c_id, connection in self.connections.items():
                if user_id != c_id:
                    try:
                        connection.c_out.send(data)
                    except BrokenPipeError:
                        self.connections.pop(c_id, None)

    def init_id(self, user_id):
        try:
            self.connections[user_id]
        except KeyError:

            class Cons:
                def __init__(self):
                    self.c_in = None
                    self.c_out = None

            self.connections[user_id] = Cons()

    def run_server_in(self):
        while True:
            c, addr = self.socket_in.accept()
            user_id = c.recv(2048)

            self.init_id(user_id)

            self.connections[user_id].c_in = c

            threading.Thread(target=self.run_client, args=(
                user_id,
                c,
            )).start()

    def run_server_out(self):
        while True:
            c, addr = self.socket_out.accept()
            user_id = c.recv(2048)

            self.init_id(user_id)

            self.connections[user_id].c_out = c


def user_mic_thread():
    pass


def user_speaker_thread():
    pass


def channel_thread():
    pass


def endpoint_thread():
    pass


if __name__ == "__main__":
    server = SocketSoundServer(10000, 10001, '')
    server.start()
