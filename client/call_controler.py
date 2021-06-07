from connectors.sound import DeviceSoundOutputConnector, DeviceSoundInputConnector
from connectors.server import ServerSoundOutputConnector, ServerSoundInputConnector
from connectors.pipe import ConnectorPipe

from config.sound import FRAME_SIZE, SAMPLE_SIZE


class ConnectionStartedError(ConnectionError):
    pass


class ConnectionNotStartedError(ConnectionError):
    pass


class CallController:
    user_id: int
    url: str
    mic_port: int
    speaker_port: int
    mic_pipe: ConnectorPipe
    speaker_pipe: ConnectorPipe
    connected: bool

    def __init__(self, url, mic_port, speaker_port, user_id):
        self.user_id = user_id
        self.url = url
        self.mic_port = mic_port
        self.speaker_port = speaker_port
        self.connected = False

    def connect(self, channel_id: int):
        print(channel_id)
        if self.connected:
            raise ConnectionStartedError()

        self.speaker_pipe = ConnectorPipe(
            ServerSoundInputConnector(
                url=self.url,
                port=self.speaker_port,
                connection_id=f'{channel_id}-{self.user_id}'
            ),
            DeviceSoundOutputConnector(
                frame_size=FRAME_SIZE,
                sample_rate=SAMPLE_SIZE
            )
        )

        self.mic_pipe = ConnectorPipe(
            DeviceSoundInputConnector(
                frame_size=FRAME_SIZE,
                sample_rate=SAMPLE_SIZE
            ),
            ServerSoundOutputConnector(
                url=self.url,
                port=self.mic_port,
                connection_id=f'{channel_id}-{self.user_id}'
            )
        )

    def disconnect(self):
        if not self.connected:
            raise ConnectionNotStartedError()

        self.mic_pipe.close()
        self.speaker_pipe.close()
