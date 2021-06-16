import time

from server import Server

if __name__ == "__main__":
    server = Server()
    server.run()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Stopping...')
        server.stop()
        time.sleep(10)
        print('Stopped')





