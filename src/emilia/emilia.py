from ollama import (
    chat,
    Message,
    ChatResponse,
)
from typing import (
    Sequence,
)

from emilia.tools import (
    search_internet,
    what_time_is_it,
)
from emilia.hardcoded import context

class Emilia:
    def __init__(self, model: str):
        self.model = model
        self.context = []
        self.tools = {
            "search_internet": search_internet,
            "what_time_is_it": what_time_is_it,
        }

        self.append_context_system(context)

    def execute_tool_call(self, call: Message.ToolCall) -> str:
        return self.tools[call.function.name](**call.function.arguments)

    def generate_content(
        self,
    ) -> tuple[Message, str | None, str | None, Sequence[Message.ToolCall] | None]:
        response = chat(
            model=self.model,
            messages=self.context,
            tools=list(self.tools.values()),
        )

        return (
            response.message,
            response.message.content,
            response.message.thinking,
            response.message.tool_calls,
        )

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
