from pathlib import Path
import pyaudio
import numpy as np
import wave

class Audio(pyaudio.PyAudio):
    def __init__(self):
        super().__init__()

        # for recording:
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024 # works in _play too

        # continuous for avoiding bugs
        self.continuous_stream = self.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
        )

    def record(self, seconds: int) -> list:
        stream = self.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
        )

        frames = []

        for _ in range(0, int(self.RATE / self.CHUNK * seconds)):
            frames.append(stream.read(self.CHUNK))

        return frames

    def play(self, file: Path):
        with wave.open(str(file), "rb") as wf:
            stream = self.open(
                format=self.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True, 
            )

            while len(data := wf.readframes(self.CHUNK)):
                stream.write(data)

            stream.stop_stream()
            stream.close()

    def play_direct(self, audio: np.ndarray, samplerate: int):
        try:
            stream = self.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=samplerate,
                output=True,
                frames_per_buffer=self.CHUNK,
            )

            stream.write(audio.astype(np.float32).tobytes())
        finally:
            pass
            #stream.stop_stream()
            #stream.close()

    def close_audio(self):
        self.continuous_stream.stop_stream()
        self.continuous_stream.close()
        self.terminate()
