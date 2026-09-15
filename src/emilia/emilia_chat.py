from emilia.emilia import Emilia
from kopilogs.paint import paint

class EmiliaChat(Emilia):
    def __init__(self, model: str):
        super().__init__(model)

    def start(self):
        while True:
            lines = []

            while True:
                line = input(paint(">>> ").bold().green())

                if line == "/bye":
                    paint("Exiting...").bold().red().show()
                    return

                if not line:
                    break

                lines.append(line)

            self.append_context_user("\n".join(lines))

            while True:
                message, content, _, tool_calls = self.generate_content()
                self.append_context_assistant(message)

                if tool_calls is None:
                    break;

                for tc in tool_calls:
                    call_content = self.execute_tool_call(tc)
                    self.append_context_tool(tc.function.name, call_content)

            print()
            paint(">>> ", end="").bold().green().show()
            print(content)
            print()
