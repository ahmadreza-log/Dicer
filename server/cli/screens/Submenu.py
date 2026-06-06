from cli.Panel import Panel


class Submenu:
    # Reusable submenu screen with a title, optional summary, and numbered options.

    @classmethod
    def Render(
        cls,
        title: str,
        options: list[tuple[str, str]],
        summary: list[str] | None = None,
    ) -> None:
        Panel.Clear()
        Panel.Banner()
        print(f"  ⚙️  {title}")
        print()

        if summary:
            Panel.Box("Overview", summary)

        for number, label in options:
            print(f"  [{number}] {label}")

        print(f"  [0] ⬅️  Back")
        print()

    @classmethod
    def Read(cls) -> str:
        try:
            Panel.Prompt()
            return input().strip()
        except EOFError:
            return "0"
