from connection.Settings import Settings
from cli.Manager import Manager
from cli.screens.Message import Message
from cli.screens.Prompt import Prompt
from cli.screens.Submenu import Submenu
from cli.settings.Summary import Summary


class Connection:
    # Connection settings submenu.

    Options = [
        ("1", "💬  Welcome Message"),
        ("2", "📦  Buffer Size"),
        ("3", "⏱️  Idle Timeout"),
        ("4", "🔢  Max Per Address"),
    ]

    @classmethod
    def Run(cls, manager: Manager) -> None:
        while True:
            Submenu.Render("Connection Settings", cls.Options, Summary.Connection())
            choice = Submenu.Read()

            if choice == "0":
                return

            actions = {
                "1": cls.ChangeWelcome,
                "2": cls.ChangeBuffer,
                "3": cls.ChangeTimeout,
                "4": cls.ChangeMaxPerAddress,
            }

            action = actions.get(choice)

            if action is None:
                Message.Render(text="Invalid choice.", kind="error")
                continue

            action(manager)

    @classmethod
    def ChangeWelcome(cls, manager: Manager) -> None:
        welcome = Prompt.Ask(
            title="Welcome Message",
            rows=[("Current:", Settings.Welcome)],
            label="New message",
        )

        if not welcome:
            Message.Render(text="Message cannot be empty.", kind="error")
            return

        Settings.Welcome = welcome
        Message.Render(text="Welcome message updated.", kind="success")

    @classmethod
    def ChangeBuffer(cls, manager: Manager) -> None:
        raw = Prompt.Ask(
            title="Buffer Size",
            rows=[("Current:", str(Settings.Buffer))],
            label="New size (bytes)",
        )

        if not raw.isdigit() or int(raw) < 256:
            Message.Render(text="Buffer must be at least 256 bytes.", kind="error")
            return

        Settings.Buffer = int(raw)
        Message.Render(text=f"Buffer size set to {raw} bytes.", kind="success")

    @classmethod
    def ChangeTimeout(cls, manager: Manager) -> None:
        raw = Prompt.Ask(
            title="Idle Timeout",
            rows=[
                ("Current:", str(Settings.Timeout)),
                ("", "0 = no timeout"),
            ],
            label="New timeout (seconds)",
        )

        if not raw.isdigit():
            Message.Render(text="Timeout must be a number.", kind="error")
            return

        Settings.Timeout = int(raw)
        label = raw if int(raw) > 0 else "disabled"
        Message.Render(text=f"Idle timeout set to {label}.", kind="success")

    @classmethod
    def ChangeMaxPerAddress(cls, manager: Manager) -> None:
        raw = Prompt.Ask(
            title="Max Per Address",
            rows=[
                ("Current:", str(Settings.MaxPerAddress)),
                ("", "0 = unlimited"),
            ],
            label="New limit",
        )

        if not raw.isdigit():
            Message.Render(text="Value must be a number.", kind="error")
            return

        Settings.MaxPerAddress = int(raw)
        label = raw if int(raw) > 0 else "unlimited"
        Message.Render(text=f"Max per address set to {label}.", kind="success")
