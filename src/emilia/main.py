from emilia import EmiliaChat
from emilia import EmiliaTalk
import sys

def main() -> int:
    args = sys.argv[1:]

    if not args:
        print("You have two options for Emilia!")
        print("\n[+] emilia chat")
        print("[+] emilia talk\n")
        return 1

    model = "tripolskypetr/qwen3.5-uncensored-aggressive:latest"

    match args[0]:
        case "talk":
            try:
                print("Unavailable temporarily.")
            except KeyboardInterrupt:
                pass

        case "chat":
            EmiliaChat(model).start()

        case _:
            print("[!] Not a valid option!\n")
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
