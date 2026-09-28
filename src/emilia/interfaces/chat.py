from emilia import Emilia

from kopilogs.paint import paint
import re

class EmiliaChat(Emilia):
    def __init__(self, model: str):
        super().__init__(model)

    def start(self):
        while True:
            lines = []

            while True:
                line = input(paint(">>> ").bold().magenta())

                if line == "/bye":
                    paint("Exiting...").bold().red().show()
                    return

                if not line:
                    break

                lines.append(line)

            content = self.generate_content_full("\n".join(lines))

            if content is not None:
                print()
                paint(">>> ", end="").bold().green().show()
                print(content)
                print()
