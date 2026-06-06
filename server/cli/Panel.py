class Panel:
    # Shared layout utilities used by all CLI screens.

    Width = 44

    # Clears the terminal screen for a fresh view.
    @classmethod
    def Clear(cls) -> None:
        print("\033[2J\033[H", end="")

    # Prints the application title banner.
    @classmethod
    def Banner(cls) -> None:
        line = "═" * cls.Width
        print()
        print(f"╔{line}╗")
        print(f"║{'🎲  Dicer Server Management Panel'.center(cls.Width)}║")
        print(f"╚{line}╝")
        print()

    # Draws a bordered box with a title and content lines.
    @classmethod
    def Box(cls, title: str, lines: list[str]) -> None:
        inner = cls.Width - 2

        print(f"  ┌{'─' * inner}┐")
        print(f"  │ {title.center(inner - 2)} │")
        print(f"  ├{'─' * inner}┤")

        for line in lines:
            clipped = line[: inner - 2]
            print(f"  │ {clipped.ljust(inner - 2)} │")

        print(f"  └{'─' * inner}┘")
        print()

    # Converts uptime seconds into a readable hours/minutes/seconds string.
    @classmethod
    def FormatUptime(cls, seconds: int) -> str:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining = seconds % 60

        if hours > 0:
            return f"{hours}h {minutes}m {remaining}s"

        if minutes > 0:
            return f"{minutes}m {remaining}s"

        return f"{remaining}s"

    # Prints the choice prompt at the bottom of a screen.
    @classmethod
    def Prompt(cls) -> None:
        print("  Enter choice: ", end="")
