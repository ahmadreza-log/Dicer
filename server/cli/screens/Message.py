from cli.Panel import Panel


class Message:
    # Screen 2 — feedback box shown after an action completes.

    Icons = {
        "success": "✅",
        "error": "⚠️",
        "info": "ℹ️",
    }

    Titles = {
        "success": "Success",
        "error": "Notice",
        "info": "Information",
    }

    @classmethod
    def Render(cls, text: str, kind: str = "info", title: str | None = None) -> None:
        Panel.Clear()
        Panel.Banner()

        icon = cls.Icons.get(kind, "ℹ️")
        heading = title or cls.Titles.get(kind, "Message")

        Panel.Box(heading, [f"{icon}  {text}"])
