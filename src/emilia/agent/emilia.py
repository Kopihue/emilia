from emilia.tools.internet     import Internet
from emilia.tools.dates        import Dates
from emilia.tools.applications import Applications
from emilia.tools.music        import Music
from emilia.lib.audio          import Audio
from emilia.agent.context      import Context

from ollama import chat, Message, ChatResponse
from kopitools import paint, log, Log
Log.text = True

from typing import Sequence, Any
import subprocess
import re

class Emilia:
    def __init__(
        self,
        model: str,
        context: Context,
        num_ctx: int,
    ):
        self.model = model
        self.num_ctx = num_ctx
        self.audio = Audio() # for music tools
        self.context = []

        self.tools = {}
        try:
            self.internet_tool = Internet()
        except RuntimeError:
            pass
        else:
            self.tools.update({
                "get_urls_from_search_queries": self.internet_tool.get_urls_from_search_queries,
                "get_content_from_urls": self.internet_tool.get_content_from_urls,
            }) 
            context.add_context_tool(Context.TOOL_INTERNET)

        try:
            self.dates_tool = Dates()
        except Exception:
            pass
        else:
            self.tools.update({
                "get_current_datetime": self.dates_tool.get_current_datetime,
            })
            context.add_context_tool(Context.TOOL_DATETIMES)

        try:
            self.music_tool = Music(self.audio.client)
        except FileNotFoundError as e:
            print(e)
        else:
            self.tools.update({
                "play_song":self.music_tool.play_song,
                "play_song_on_repeat": self.music_tool.play_song_on_repeat,
                "pause_song": self.music_tool.pause_song,
                "resume_song": self.music_tool.resume_song,
                "close_song": self.music_tool.close_song,
                "get_songs": self.music_tool.get_songs,
                "close_all_songs": self.music_tool.close_all_songs,
            })
            context.add_context_tool(Context.TOOL_MUSIC)

        self.append_context_system(str(context))
        subprocess.run("clear")

        log(
            "Using model:",
            f"[{paint(self.model).bold().magenta()}]",
        ).info()
        log(
            "Using num_ctx:",
            f"[{paint(self.num_ctx).bold().magenta()}]",
        ).info()
        log(
            "Capping num_ctx at:",
            f"[{paint(int(self.num_ctx * 0.90)).bold().magenta()}]",
        ).info()
        paint("=" * 80).bold().green().show()

    def execute_tool_call(self, call: Message.ToolCall) -> str:
        return self.tools[call.function.name](**call.function.arguments)

    def generate_content_full(self, user_message: str) -> str | None:
        self.append_context_user(user_message)

        while True:
            response = self.generate_content()
            self.append_context_assistant(response["message"])

            if response["tool_calls"] is None:
                break

            for tc in response["tool_calls"]:
                call_content = self.execute_tool_call(tc)
                self.append_context_tool(tc.function.name, call_content)

        if response["content"] is not None:
            return re.sub(r"[\*\#]", "", response["content"])

    def generate_content(
        self,
    ) -> dict[str, Any]:
        while True:
            response: ChatResponse = chat(
                model=self.model,
                messages=self.context,
                tools=list(self.tools.values()),
                options={
                    "num_ctx": self.num_ctx,
                    "num_predict": -1 ,
                },
            )

            if response.prompt_eval_count is not None:
                if response.prompt_eval_count > int(self.num_ctx * 0.90):
                    paint("Cleaning context...").bold().blue().show()
                    self.context = self.context[0] + self.context[-2:]
                    continue
            break

        return {
            "message": response.message,
            "content": response.message.content,
            "thinking": response.message.thinking,
            "tool_calls": response.message.tool_calls,
            "done": response.done,
            "done_reason": response.done_reason,
        }

    def append_context_system(self, content: str):
        self.context.append({
            "role": "system",
            "content": content,
        })

    def append_context_user(self, content: str):
        self.context.append({
            "role": "user",
            "content": content,
        })

    def append_context_assistant(self, message: Message):
        self.context.append(message)

    def append_context_tool(self, name: str, content: str):
        self.context.append({
            "role": "tool",
            "tool_name": name,
            "content": content,
        })

    def exit(self):
        paint("Exiting...").bold().red().show()
        self.music_tool.close_all_songs()
        self.audio.close()
