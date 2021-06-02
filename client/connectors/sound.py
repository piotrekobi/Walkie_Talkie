from generic_connectors import OutputConnector, InputConnector

import sounddevice as sd


class DeviceSoundOutputConnector(OutputConnector):
    frame_size: int
    sample_rate: int
    stream: sd.OutputStream

    def __init__(self, frame_size: int, sample_rate: int):
        self.frame_size = frame_size
        self.sample_rate = sample_rate

        super().__init__()
        self.name = "SoundOutputConnector"

    def setup(self):
        self.logger.log(1, 'Starting Thread')
        self.stream = sd.OutputStream(
            channels=1,
            dtype='float32',
            blocksize=self.frame_size,
            samplerate=self.sample_rate
        )

        self.stream.start()

    def read_frame(self, data):
        try:
            self.stream.write(data)
        except Exception as e:
            self.logger.error(e)

    def destroy(self):
        self.logger.log(1, 'Stoping Thread')
        self.stream.close()


class DeviceSoundInputConnector(InputConnector):
    frame_size: int
    sample_rate: int
    stream: sd.InputStream

    def __init__(self, frame_size: int, sample_rate: int):
        self.frame_size = frame_size
        self.sample_rate = sample_rate

        super().__init__()
        self.name = "SoundInputConnector"

    def setup(self):
        self.stream = sd.InputStream(
            channels=1,
            dtype='float32',
            blocksize=self.frame_size,
            samplerate=self.sample_rate
        )

        self.stream.start()

    async def await_frame(self):
        try:
            return self.stream.read(self.frame_size)
        except Exception as e:
            self.logger.error(e)

    def destroy(self):
        self.logger.log(1, 'Stoping Thread')
        self.stream.close()
