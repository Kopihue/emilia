from emilia.emilia_chat import EmiliaChat
import sys

def main() -> int:
    emilia = EmiliaChat("qwen3").start()

    return 0

if __name__ == "__main__":
    sys.exit(main())
