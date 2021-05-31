import socket
import threading


class SocketSoundServer:
    def __init__(self, port, address):
        self.connections = []
        self.server = None
        self.socket = None
        self.ip = address
        self.port = port

    def start(self):
        self.socket = socket.socket()
        print("Socket successfully created")

        self.socket.bind((self.ip, self.port))
        print(f"socket binded to {self.port}")

        self.socket.listen(5)
        print("socket is listening")

        self.server = threading.Thread(target=self.run_server)
        self.server.start()

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

    def run_client(self, current_connection):
        while True:
            data = current_connection.recv(9000)
            for connection in self.connections:
                if current_connection != connection:
                    try:
                        connection.send(data)
                    except BrokenPipeError:
                        self.connections.remove(connection)

    def run_server(self):
        while True:
            c, addr = self.socket.accept()
            self.connections.append(c)
            threading.Thread(target=self.run_client, args=(c,)).start()


if __name__ == "__main__":
    server = SocketSoundServer(10000, '')
    server.start()
