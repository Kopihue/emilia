from emilia import Emilia
from emilia.lib import Kokoro
from emilia.lib import TempFile
from emilia.lib import Whisper
from emilia.lib import Audio
from emilia.agent import Context

from kopilogs.paint import paint

from concurrent.futures import ThreadPoolExecutor
import time
import subprocess

class EmiliaTalk(Emilia):
    def __init__(self, model: str, context: Context):
        super().__init__(model, context)

        self.whisper = Whisper()
        self.kokoro = Kokoro()

        # remove noise
        subprocess.run("clear")

    def terminate(self):
        self.audio.close()

class EmiliaTalkStartWithKey(EmiliaTalk):
    def __init__(self, model: str, context: Context):
        super().__init__(model, context)
        self.key = False
        self.temp_file = TempFile()

    def start(self):
        with ThreadPoolExecutor() as exec:
            exec.submit(self._toggle_key)
            exec.submit(self._start_if_key)

    def _toggle_key(self):
        paint("Press <ENTER> to toggle!").bold().red().show()

        while True:
            input("")
            self.key = not self.key

    def _start_if_key(self):
        frames = []

        while True:
            while self.key:
                print("Recording...")
                chunk = self.audio.record(1)
                frames.extend(chunk)

            if frames:
                self.temp_file.save_to_wav(
                    channels=self.audio.CHANNELS,
                    framerate=self.audio.RATE,
                    sampwidth=self.audio.get_sample_size(self.audio.FORMAT),
                    frames=frames,
                )
                transcribe = self.whisper.transcribe(self.temp_file.get())
                self.temp_file.clear()

                paint(
                    paint(">>>").bold().magenta(),
                    paint(transcribe),
                ).show()

                content = self.generate_content_full(transcribe)

                if content is not None:
                    paint(
                        paint(">>>").bold().magenta(),
                        paint(content),
                    ).show()

                    for rendered in self.kokoro.get_sentence(content):
                        self.audio.play_direct(rendered, 24_000)

                frames.clear()

            time.sleep(0.01)

class EmiliaTalkStartWithVoice(EmiliaTalk):
    def __init__(self, model: str):
        super().__init__(model)
        self.queue = []
