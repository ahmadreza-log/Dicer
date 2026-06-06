from config.Store import Store
from cli.Manager import Manager
from cli.screens.Message import Message
from cli.screens.Submenu import Submenu
from cli.settings.Summary import Summary


class Persist:
    # Save, load, and reset settings submenu.

    Options = [
        ("1", "💾  Save Settings"),
        ("2", "📂  Load Settings"),
        ("3", "♻️  Reset to Defaults"),
    ]

    @classmethod
    def Run(cls, manager: Manager) -> None:
        while True:
            Submenu.Render("Save / Load / Reset", cls.Options, Summary.Persist())
            choice = Submenu.Read()

            if choice == "0":
                return

            actions = {
                "1": cls.Save,
                "2": cls.Load,
                "3": cls.Reset,
            }

            action = actions.get(choice)

            if action is None:
                Message.Render(text="Invalid choice.", kind="error")
                continue

            action(manager)

    @classmethod
    def Save(cls, manager: Manager) -> None:
        success, message = Store.Save()
        kind = "success" if success else "error"
        Message.Render(text=message, kind=kind)

    @classmethod
    def Load(cls, manager: Manager) -> None:
        if manager.IsActive():
            Message.Render(
                text="Stop the server before loading settings.",
                kind="error",
            )
            return

        success, message = Store.Load()
        kind = "success" if success else "error"
        Message.Render(text=message, kind=kind)

    @classmethod
    def Reset(cls, manager: Manager) -> None:
        if manager.IsActive():
            Message.Render(
                text="Stop the server before resetting settings.",
                kind="error",
            )
            return

        success, message = Store.Reset()
        kind = "success" if success else "error"
        Message.Render(text=message, kind=kind)
