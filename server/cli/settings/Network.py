from config.Settings import ResolveHost
from config.Settings import Settings
from cli.Manager import Manager
from cli.screens.Message import Message
from cli.screens.Prompt import Prompt
from cli.screens.Submenu import Submenu
from cli.settings.Input import Input
from cli.settings.Summary import Summary


class Network:
    # Network settings submenu.

    Options = [
        ("1", "🌐  Change Host"),
        ("2", "🔌  Change Port"),
        ("3", "📡  Listen Mode"),
        ("4", "👥  Max Clients"),
        ("5", "🚀  Auto Start"),
    ]

    @classmethod
    def Run(cls, manager: Manager) -> None:
        while True:
            Submenu.Render("Network Settings", cls.Options, Summary.Network())
            choice = Submenu.Read()

            if choice == "0":
                return

            actions = {
                "1": cls.ChangeHost,
                "2": cls.ChangePort,
                "3": cls.ChangeMode,
                "4": cls.ChangeMaxClients,
                "5": cls.ToggleAutoStart,
            }

            action = actions.get(choice)

            if action is None:
                Message.Render(text="Invalid choice.", kind="error")
                continue

            action(manager)

    # Stops the server, applies a network change, and restarts if it was running.
    @classmethod
    def Apply(cls, manager: Manager, success_text: str) -> None:
        success, message = manager.ReloadAfterNetworkChange()

        if success:
            Message.Render(text=f"{success_text} {message}", kind="success")
        else:
            Message.Render(text=message, kind="error")

    @classmethod
    def ChangeHost(cls, manager: Manager) -> None:
        host = Prompt.Ask(
            title="Change Host",
            rows=[("Current:", Settings.Host), ("Mode:", Settings.Mode)],
            label="New host",
        )

        if not host:
            Message.Render(text="Host cannot be empty.", kind="error")
            return

        Settings.Host = host
        Settings.Mode = "Custom"
        cls.Apply(manager, f"Host set to {host}.")

    @classmethod
    def ChangePort(cls, manager: Manager) -> None:
        raw = Prompt.Ask(
            title="Change Port",
            rows=[("Current:", str(Settings.Port))],
            label="New port",
        )

        if not raw.isdigit():
            Message.Render(text="Port must be a number.", kind="error")
            return

        port = int(raw)

        if port < 1 or port > 65535:
            Message.Render(text="Port must be between 1 and 65535.", kind="error")
            return

        Settings.Port = port
        cls.Apply(manager, f"Port set to {port}.")

    @classmethod
    def ChangeMode(cls, manager: Manager) -> None:
        mode = Input.PickMode(Settings.Mode)

        if mode is None:
            return

        Settings.Mode = mode
        bind = ResolveHost()
        cls.Apply(manager, f"Listen mode set to {mode} ({bind}).")

    @classmethod
    def ChangeMaxClients(cls, manager: Manager) -> None:
        raw = Prompt.Ask(
            title="Max Clients",
            rows=[
                ("Current:", str(Settings.MaxClients)),
                ("", "0 = unlimited"),
            ],
            label="New limit",
        )

        if not raw.isdigit():
            Message.Render(text="Value must be a number.", kind="error")
            return

        Settings.MaxClients = int(raw)
        label = raw if int(raw) > 0 else "unlimited"
        Message.Render(text=f"Max clients set to {label}.", kind="success")

    @classmethod
    def ToggleAutoStart(cls, manager: Manager) -> None:
        Settings.AutoStart = Input.Toggle("Auto Start", Settings.AutoStart)
        state = "enabled" if Settings.AutoStart else "disabled"
        Message.Render(text=f"Auto start {state}.", kind="success")
