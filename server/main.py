from server import Server
from flask_runner import FlaskRunner

if __name__ == "__main__":
    try:
        server = Server()
        server.run()

        flask = FlaskRunner()
        flask.run()
    except KeyboardInterrupt:
        print('Stopping...')
        server.stop()
