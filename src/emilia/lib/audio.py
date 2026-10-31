import pyaudio

from pathlib import Path
from typing import Callable
import wave
import time

class Audio:
    def __init__(self):
        self.client = pyaudio.PyAudio()

        # continuous for input
        self.continuous_stream = self.client.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
        )

    def record(self, seconds: float) -> list:
        frames = []
        rate = 44100
        chunk = 1024

        for _ in range(0, int(rate / chunk * seconds)):
            frames.append(self.continuous_stream.read(chunk))

        return frames

    def play_numpy_array(self, audio: np.ndarray, samplerate: int):
        chunk = 1024

        try:
            stream = self.client.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=samplerate,
                output=True,
                frames_per_buffer=chunk,
            )

            stream.write(audio.astype(np.float32).tobytes())

        finally:
            stream.stop_stream()
            stream.close()

    def close(self):
        self.continuous_stream.stop_stream()
        self.continuous_stream.close()
        self.client.terminate()













class AudioFile:
    CHUNK = 1024

    def __init__(self, client: pyaudio.PyAudio, file: Path, callback: Callable):
        self.client = client
        self.file = file
        self.callback = callback
        self.wf = wave.open(str(self.file), "rb")
        self.stream: pyaudio.Stream = self.client.open(
            format=self.client.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            output=True,
        )

        self.playing = False
        self.running = False

        self.thread = Thread(target=self._play)

    def pause(self):
        self.playing = False

    def resume(self):
        self.playing = True

    def close(self):
        self.playing = False
        self.running = False
        self.thread.join()

    def wait(self, timeout: None | int = None):
        self.thread.join(timeout=timeout)

        if self.thread.is_alive():
            self.close()

    def play(self):
        self.running = True
        self.playing = True
        self.thread.start()

    def _play(self):
        while self.running:
            if not self.playing:
                time.sleep(0.1)
                continue

            frames = self.wf.readframes(AudioFile.CHUNK)

            if not frames:
                self.running = False
                self.playing = False
                break

            self.stream.write(frames)

        self._clean()
        self.callback(self)

    def _clean(self):
        self.wf.close()
        self.stream.stop_stream()
        self.stream.close()
