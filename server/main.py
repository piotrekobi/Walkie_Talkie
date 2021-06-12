import os

from server import Server
from flask_runner import FlaskRunner


def child():
    flask = FlaskRunner()
    flask.run()


def parent():
    server = Server()
    server.run()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Stopping...')
        server.stop()


if __name__ == "__main__":
    newpid = os.fork()
    if newpid == 0:
        child()
    else:
        parent()





