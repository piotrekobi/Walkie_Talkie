from server import Server


if __name__ == "__main__":
    server = Server()
    server.run()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Stopping...')
        server.stop()
