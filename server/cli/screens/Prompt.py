from cli.Panel import Panel


class Prompt:
    # Input screen for settings that require user text entry.

    @classmethod
    def Ask(cls, title: str, rows: list[tuple[str, str]], label: str) -> str:
        Panel.Clear()
        Panel.Banner()

        lines = [f"{name:<16} {value}" for name, value in rows]
        lines.append("")
        lines.append(f"{label}:")

        Panel.Box(title, lines)

        try:
            return input(f"  {label}: ").strip()
        except EOFError:
            return ""
