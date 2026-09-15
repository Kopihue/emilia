from emilia.emilia_chat import EmiliaChat
from emilia.emilia_talk import EmiliaTalk
import sys

def main() -> int:
    EmiliaChat("qwen3").start()

    return 0

if __name__ == "__main__":
    sys.exit(main())
