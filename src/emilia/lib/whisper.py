from pathlib import Path
import whisper

class Whisper:
    def __init__(self):
        self.model = whisper.load_model("base.en")

    def transcribe(self, file: Path) -> str:
        return self.model.transcribe(str(file))["text"]
