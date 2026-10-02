from emilia import EmiliaChat
from emilia import EmiliaTalk
import sys

def main() -> int:
    args = sys.argv[1:]

    if not args:
        print("You have these options for Emilia!")
        print("[+] emilia chat\n")
        return 1

    model = "tripolskypetr/qwen3.5-uncensored-aggressive:latest"

    match args[0]:
        case "talk":
            try:
                talk = EmiliaTalk(model)
                talk.start()
            except Exception as e:
                print(e)
                return 1

        case "chat":
            EmiliaChat(model).start()

        case _:
            print("[!] Not a valid option!\n")
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
