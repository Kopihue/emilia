from emilia.agent import context
from emilia.tools import (
    get_urls_from_search_queries,
    get_content_from_urls,
    get_current_datetime,
)

from ollama import (
    chat,
    Message,
    ChatResponse,
)
from typing import Sequence, Any
from kopilogs.paint import paint

import re

class Emilia:
    def __init__(self, model: str):
        self.model = model
        self.context = []
        self.tools = {
            "get_urls_from_search_queries": get_urls_from_search_queries,
            "get_content_from_urls": get_content_from_urls,
            "get_current_datetime": get_current_datetime,
        }

        self.append_context_system(context)

    def execute_tool_call(self, call: Message.ToolCall) -> str:
        paint(
            paint("Executing tool:"),
            paint(call.function.name).bold().green(),
            paint("|"),
            paint(call.function.arguments).bold().magenta(),
        ).show()
        return self.tools[call.function.name](**call.function.arguments)

    def generate_content_full(self, user_message: str) -> str | None:
        self.append_context_user(user_message)

        while True:
            response = self.generate_content()
            print(response["thinking"])
            self.append_context_assistant(response["message"])

            if response["tool_calls"] is None:
                break;

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
                    "num_ctx": 32_768,
                    "num_predict": -1 ,
                },
            )

            if response.prompt_eval_count is not None:
                if response.prompt_eval_count > 28_000:
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
