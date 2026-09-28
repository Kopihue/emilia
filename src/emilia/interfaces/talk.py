from emilia import Emilia
from emilia.lib import Kokoro
from emilia.lib import TempFile
from emilia.lib import Whisper
from emilia.lib import Audio

from kopilogs.paint import paint

from concurrent.futures import ThreadPoolExecutor
import time
import random
import re
import subprocess

class EmiliaTalk(Emilia):
    def __init__(self, model: str):
        super().__init__(model)

        self.keyword = False
        self.audio = Audio()
        self.whisper = Whisper()
        self.kokoro = Kokoro()
        self.queue: list[TempFile] = []

        # remove noise
        subprocess.run("clear")

    def start(self):
        with ThreadPoolExecutor() as exec:
            exec.submit(self._save_audio)
            exec.submit(self._find_keyword)
            exec.submit(self._execute_if_keyword)

    def _execute_if_keyword(self):
        while True:
            paint("Ready...").bold().blue().show()
            while not self.keyword:
                time.sleep(0.01)

            # pause threads
            self._clear_queue()

            try:
                intros = [
                    "Yeah?",
                    "Tell me!",
                    "What's up!",
                    "Hey!",
                    "Yup!",
                ]
                choice = random.choice(intros)
                print(choice)

                for rendered in self.kokoro.get_sentence(choice):
                    self.audio.play_direct(rendered, 24_000)

                result = self._get_twenty_seconds()
                print()
                paint(">>> ", end="").bold().magenta().show()
                print(result)
                print()

                content = self.generate_content_full(result)

                if content is not None:
                    print()
                    paint(">>> ", end="").bold().green().show()
                    print(content)
                    print()

                    for rendered in self.kokoro.get_sentence(content):
                        self.audio.play_direct(rendered, 24_000)
            finally:
                self._clear_queue()

    def _find_keyword(self):
        keywords = [
            "emilia",
            "amelia",
            "emily",
        ]

        while True:
            try:
                file = self.queue.pop(0)
            except IndexError:
                time.sleep(0.1)
                continue

            transcribed = self.whisper.transcribe(file.get()).lower()
            file.delete()

            found = False
            for kw in keywords:
                if kw in transcribed:
                    found = True

            self.keyword = found

    def _get_twenty_seconds(self) -> str:
        temp = TempFile()
        temp.save_to_wav(
            channels=self.audio.CHANNELS,
            framerate=self.audio.RATE,
            sampwidth=self.audio.get_sample_size(self.audio.FORMAT),
            frames=self.audio.record(5),
        )

        result = self.whisper.transcribe(temp.get())
        temp.delete()

        return result

    def _save_audio(self):
        while True:
            temp = TempFile()
            temp.save_to_wav(
                channels=self.audio.CHANNELS,
                framerate=self.audio.RATE,
                sampwidth=self.audio.get_sample_size(self.audio.FORMAT),
                frames=self.audio.record(2),
            )

            self.queue.append(temp)

    def _clear_queue(self):
        for file in self.queue:
            file.delete()

        self.queue.clear()

    def terminate(self):
        self.audio.close_audio()
        self._clear_queue()
