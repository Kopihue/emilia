from emilia.agent.context import Context
from emilia.agent.emilia  import Emilia

from kopitools import paint
import re

class EmiliaChat(Emilia):
    def __init__(self, model: str, context: Context, num_ctx: int):
        super().__init__(model, context, num_ctx)

    def start(self):
        while True:
            lines = []

            while True:
                line = input(paint(">>> ").bold().blue())

                if line == "/bye":
                    self.exit()
                    return

                if not line:
                    break

                lines.append(line)

            content = self.generate_content_full("\n".join(lines))

            if content is not None:
                print()
                paint(">>> ", end="").bold().magenta().show()
                print(content)
                print()
