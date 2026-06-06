import sys


class Terminal:
    # Ensures the terminal supports UTF-8 output for emojis and box characters.

    Configured = False

    @classmethod
    def Configure(cls) -> None:
        if cls.Configured:
            return

        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")

        if hasattr(sys.stdin, "reconfigure"):
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")

        cls.Configured = True
