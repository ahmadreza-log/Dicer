from cli.Manager import Manager
from cli.screens.Detail import Detail
from cli.screens.Message import Message
from cli.screens.Submenu import Submenu
from cli.settings.Connection import Connection as ConnectionMenu
from cli.settings.Database import Database as DatabaseMenu
from cli.settings.Logging import Logging
from cli.settings.Network import Network as NetworkMenu
from cli.settings.Persist import Persist
from cli.settings.Security import Security
from cli.settings.Summary import Summary


class Hub:
    # Main settings hub with links to every settings category.

    Options = [
        ("1", "🌐  Network Settings"),
        ("2", "📊  Logging Settings"),
        ("3", "🔗  Connection Settings"),
        ("4", "🔒  Security Settings"),
        ("5", "🗄️  Database Settings"),
        ("6", "💾  Save / Load / Reset"),
        ("7", "📋  View All Settings"),
    ]

    @classmethod
    def Run(cls, manager: Manager) -> None:
        while True:
            Submenu.Render("Settings", cls.Options, Summary.All(manager))
            choice = Submenu.Read()

            if choice == "0":
                return

            actions = {
                "1": lambda: NetworkMenu.Run(manager),
                "2": lambda: Logging.Run(manager),
                "3": lambda: ConnectionMenu.Run(manager),
                "4": lambda: Security.Run(manager),
                "5": lambda: DatabaseMenu.Run(manager),
                "6": lambda: Persist.Run(manager),
                "7": lambda: cls.ViewAll(manager),
            }

            action = actions.get(choice)

            if action is None:
                Message.Render(text="Invalid choice.", kind="error")
                continue

            action()

    @classmethod
    def ViewAll(cls, manager: Manager) -> None:
        Detail.Render(
            title="All Settings",
            rows=Summary.AllRows(manager),
        )
