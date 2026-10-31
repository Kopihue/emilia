from emilia.interfaces.chat import EmiliaChat
from emilia.agent.context import Context

from kopitools import (
    paint,
    log, Log,
    Registry, Args,
    EntryPointNotFoundError, ArgError,
)
Log.text = True

import sys

def main() -> int:
    try:
        main = get_main_options()
    except ArgError as e:
        log(e).critical()
        return 1

    chat, voice = get_chat_options(), get_voice_options()
    context = Context()

    if chat is not None and voice is not None:
        log("You can only choose one action at a time!").error()
        return 1

    elif chat is not None:
        EmiliaChat(main["llm_model"], context, main["num_ctx"]).start()

    elif voice is not None:
        start_voice_actions()

    else:
        paint(
            paint("You need to choose at least one!\n").bold(),
            paint("[*] Chat\n").bold().blue(),
            paint("[*] Talk").bold().magenta(),
            sep="",
        ).show()
        return 1

    return 0

def get_main_options() -> Args:
    main = Registry(sys.argv)

    main.option(
        "--llm-model",
        receives=str,
        default="tripolskypetr/qwen3.5-uncensored-aggressive:latest",
        attribute="llm_model",
    )
    main.option(
        "--num-ctx",
        receives=int,
        default=32_768,
        attribute="num_ctx",
    )

    return main.collect()

def get_chat_options() -> Args | None:
    try:
        chat = Registry(sys.argv, entry_point="chat")
    except EntryPointNotFoundError:
        return None

    return chat.collect()

def get_voice_options() -> Args | None:
    try:
        voice = Registry(sys.argv, entry_point="talk")
    except EntryPointNotFoundError:
        return None

    return voice.collect()

def start_voice_actions():
    try:
        from emilia.interfaces.talk import EmiliaTalkStartWithKey
        from emilia.interfaces.talk import EmiliaTalkStartWithVoice
    except ImportError:
        paint(
            paint("Install the voice dependencies to use the").bold().blue(),
            paint("talking").bold().magenta(),
            paint("interfaces").bold().blue(),
        ).show()
        paint(
            paint("pip install").bold().yellow(),
            paint("emilia[voice]").bold().green(),
        ).show()
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())
