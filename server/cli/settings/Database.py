from database.Engine import Engine
from database.Settings import Settings
from cli.Manager import Manager
from cli.screens.Message import Message
from cli.screens.Prompt import Prompt
from cli.screens.Submenu import Submenu
from cli.settings.Summary import Summary


class Database:
    # Database settings submenu for MySQL configuration.

    Options = [
        ("1", "🗄️  Toggle Database"),
        ("2", "🌐  Change Host"),
        ("3", "🔌  Change Port"),
        ("4", "👤  Change User"),
        ("5", "🔑  Change Password"),
        ("6", "📁  Change Database Name"),
        ("7", "🧪  Test Connection"),
        ("8", "🔗  Connect / Disconnect"),
    ]

    @classmethod
    def Run(cls, manager: Manager) -> None:
        while True:
            Submenu.Render("Database Settings", cls.Options, Summary.Database())
            choice = Submenu.Read()

            if choice == "0":
                return

            actions = {
                "1": cls.ToggleEnabled,
                "2": cls.ChangeHost,
                "3": cls.ChangePort,
                "4": cls.ChangeUser,
                "5": cls.ChangePassword,
                "6": cls.ChangeName,
                "7": cls.Test,
                "8": cls.ToggleConnect,
            }

            action = actions.get(choice)

            if action is None:
                Message.Render(text="Invalid choice.", kind="error")
                continue

            action(manager)

    @classmethod
    def Apply(cls, success_text: str) -> None:
        success, message = Engine.Reload()

        if success:
            Message.Render(text=f"{success_text} {message}", kind="success")
        else:
            Message.Render(text=message, kind="error")

    @classmethod
    def ToggleEnabled(cls, manager: Manager) -> None:
        Settings.Enabled = not Settings.Enabled

        if Settings.Enabled:
            success, message = Engine.Connect()
            kind = "success" if success else "error"
            Message.Render(text=message, kind=kind)
        else:
            Engine.Disconnect()
            Message.Render(text="Database disabled and disconnected.", kind="success")

    @classmethod
    def ChangeHost(cls, manager: Manager) -> None:
        host = Prompt.Ask(
            title="Database Host",
            rows=[("Current:", Settings.Host)],
            label="New host",
        )

        if not host:
            Message.Render(text="Host cannot be empty.", kind="error")
            return

        Settings.Host = host
        cls.Apply(f"Host set to {host}.")

    @classmethod
    def ChangePort(cls, manager: Manager) -> None:
        raw = Prompt.Ask(
            title="Database Port",
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
        cls.Apply(f"Port set to {port}.")

    @classmethod
    def ChangeUser(cls, manager: Manager) -> None:
        user = Prompt.Ask(
            title="Database User",
            rows=[("Current:", Settings.User)],
            label="New user",
        )

        if not user:
            Message.Render(text="User cannot be empty.", kind="error")
            return

        Settings.User = user
        cls.Apply(f"User set to {user}.")

    @classmethod
    def ChangePassword(cls, manager: Manager) -> None:
        masked = "********" if Settings.Password else "(empty)"
        password = Prompt.Ask(
            title="Database Password",
            rows=[("Current:", masked)],
            label="New password",
        )

        Settings.Password = password
        cls.Apply("Database password updated.")

    @classmethod
    def ChangeName(cls, manager: Manager) -> None:
        name = Prompt.Ask(
            title="Database Name",
            rows=[("Current:", Settings.Name)],
            label="New name",
        )

        if not name:
            Message.Render(text="Database name cannot be empty.", kind="error")
            return

        Settings.Name = name
        cls.Apply(f"Database name set to {name}.")

    @classmethod
    def Test(cls, manager: Manager) -> None:
        success, message = Engine.Test()
        kind = "success" if success else "error"
        Message.Render(text=message, kind=kind)

    @classmethod
    def ToggleConnect(cls, manager: Manager) -> None:
        if not Settings.Enabled:
            Message.Render(text="Enable the database in settings first.", kind="error")
            return

        if Engine.IsActive():
            Engine.Disconnect()
            Message.Render(text="Database disconnected.", kind="success")
        else:
            success, message = Engine.Connect()
            kind = "success" if success else "error"
            Message.Render(text=message, kind=kind)
