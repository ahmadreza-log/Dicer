from security.Settings import Settings
from cli.Manager import Manager
from cli.screens.Message import Message
from cli.screens.Prompt import Prompt
from cli.screens.Submenu import Submenu
from cli.settings.Summary import Summary


class Security:
    # Security settings submenu.

    Options = [
        ("1", "🔑  Server Password"),
        ("2", "✅  Allowed IPs"),
        ("3", "🚫  Blocked IPs"),
    ]

    @classmethod
    def Run(cls, manager: Manager) -> None:
        while True:
            Submenu.Render("Security Settings", cls.Options, Summary.Security())
            choice = Submenu.Read()

            if choice == "0":
                return

            actions = {
                "1": cls.ChangePassword,
                "2": cls.ChangeAllowed,
                "3": cls.ChangeBlocked,
            }

            action = actions.get(choice)

            if action is None:
                Message.Render(text="Invalid choice.", kind="error")
                continue

            action(manager)

    @classmethod
    def ChangePassword(cls, manager: Manager) -> None:
        masked = "********" if Settings.Password else "(empty)"
        password = Prompt.Ask(
            title="Server Password",
            rows=[
                ("Current:", masked),
                ("", "Leave empty to disable"),
            ],
            label="New password",
        )

        Settings.Password = password
        state = "set" if password else "cleared"
        Message.Render(text=f"Server password {state}.", kind="success")

    @classmethod
    def ChangeAllowed(cls, manager: Manager) -> None:
        allowed = Prompt.Ask(
            title="Allowed IPs",
            rows=[
                ("Current:", Settings.Allowed or "(all allowed)"),
                ("", "Comma-separated, e.g. 127.0.0.1, 10.0.0.5"),
            ],
            label="New list",
        )

        Settings.Allowed = allowed
        Message.Render(text="Allowed IP list updated.", kind="success")

    @classmethod
    def ChangeBlocked(cls, manager: Manager) -> None:
        blocked = Prompt.Ask(
            title="Blocked IPs",
            rows=[
                ("Current:", Settings.Blocked or "(none)"),
                ("", "Comma-separated"),
            ],
            label="New list",
        )

        Settings.Blocked = blocked
        Message.Render(text="Blocked IP list updated.", kind="success")
