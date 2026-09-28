from kokoro import KPipeline
import numpy as np

from typing import Iterator

class Kokoro:
    def __init__(self):
        self.pipeline = KPipeline(lang_code='a')

    def get_sentence(self, text: str) -> Iterator[np.ndarray]:
        generator = self.pipeline(text, voice='af_heart', speed=1.1)

        for _, _, audio in generator:
            yield audio.numpy()
