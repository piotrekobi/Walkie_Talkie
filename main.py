import sounddevice as sd
import soundfile as sf
import numpy as np

sr = 44100
duration = 3
myrecording = sd.rec(int(duration * sr), samplerate=sr, channels=1)
sd.wait()
sd.playrec(myrecording, sr, channels=1)
sd.wait()
# sf.write("test_recording.wav", myrecording, sr)


