from pathlib import Path
import tempfile
import wave

class TempFile:
    def __init__(self):
        file = tempfile.NamedTemporaryFile(delete=False)
        self.path = Path(file.name)
        file.close()

    def get(self) -> Path:
        return self.path

    def save_to_wav(
        self,
        channels: int,
        framerate: int,
        sampwidth: int,
        frames: list,
    ):
        with wave.open(str(self.path), "wb") as wf:
            wf.setnchannels(channels)
            wf.setframerate(framerate)
            wf.setsampwidth(sampwidth)
            wf.writeframes(b"".join(frames))

    def delete(self):
        self.path.unlink()
