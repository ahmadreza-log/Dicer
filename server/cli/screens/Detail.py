from cli.Panel import Panel


class Detail:
    # Screen 3 — detailed information display for status, clients, and settings.

    @classmethod
    def Render(cls, title: str, rows: list[tuple[str, str]]) -> None:
        Panel.Clear()
        Panel.Banner()

        lines = [f"{label:<16} {value}" for label, value in rows]
        Panel.Box(title, lines)
        cls.Wait()

    # Renders a numbered list inside a detail box (used for client lists).
    @classmethod
    def RenderList(cls, title: str, items: list[str], empty: str) -> None:
        Panel.Clear()
        Panel.Banner()

        if items:
            lines = [f"{index}. {item}" for index, item in enumerate(items, start=1)]
        else:
            lines = [empty]

        Panel.Box(title, lines)
        cls.Wait()

    # Waits for user input before returning to the previous menu.
    @classmethod
    def Wait(cls) -> None:
        try:
            Panel.Prompt()
            input()
        except EOFError:
            pass
