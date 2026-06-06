from cli.screens.Message import Message
from cli.screens.Prompt import Prompt


class Input:
    # Shared input helpers for settings submenus.

    @staticmethod
    def Toggle(label: str, current: bool) -> bool:
        state = "Yes" if current else "No"
        raw = Prompt.Ask(
            title="Toggle Setting",
            rows=[(f"{label}:", state), ("", "Enter 1 for Yes, 0 for No")],
            label="Choice",
        )

        if raw == "1":
            return True

        if raw == "0":
            return False

        Message.Render(text="Invalid choice. Use 1 or 0.", kind="error")
        return current

    @staticmethod
    def PickMode(current: str) -> str | None:
        raw = Prompt.Ask(
            title="Listen Mode",
            rows=[
                ("Current:", current),
                ("", "1 = Local (127.0.0.1)"),
                ("", "2 = Network (0.0.0.0)"),
                ("", "3 = Custom (use Host setting)"),
            ],
            label="Choice",
        )

        modes = {"1": "Local", "2": "Network", "3": "Custom"}

        if raw in modes:
            return modes[raw]

        if raw == "":
            return None

        Message.Render(text="Invalid choice. Use 1, 2, or 3.", kind="error")
        return None
