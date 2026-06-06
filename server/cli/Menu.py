from config.Settings import Settings as Network
from config.Store import Store
from database.Engine import Engine
from database.Settings import Settings as Database
from cli.Manager import Manager
from cli.Panel import Panel
from cli.screens.Detail import Detail
from cli.screens.Main import Main
from cli.screens.Message import Message
from cli.settings.Hub import Hub


class Menu:
    # Interactive text menu for managing the server without writing code.
    # Flow: Main screen → action → Message or Detail screen → Main screen.

    # Starts the main menu loop.
    @classmethod
    def Run(cls) -> None:
        Store.Load()

        manager = Manager()

        if Network.AutoStart:
            success, message = manager.Start()

            if not success:
                Message.Render(text=message, kind="error", title="Startup Failed")

        if Database.Enabled:
            success, message = Engine.Connect()

            if not success:
                Message.Render(text=message, kind="error", title="Database Failed")

        try:
            while True:
                Main.Render(manager)
                choice = cls.ReadChoice()

                if choice == "0":
                    cls.Exit(manager)
                    break

                cls.Handle(manager, choice)
        finally:
            manager.Cleanup()

            if Database.Enabled or Engine.IsActive():
                Engine.Disconnect()

    # Reads the user menu choice from the main screen.
    @classmethod
    def ReadChoice(cls) -> str:
        try:
            Panel.Prompt()
            return input().strip()
        except EOFError:
            return "0"

    # Routes the user choice to the correct action handler.
    @classmethod
    def Handle(cls, manager: Manager, choice: str) -> None:
        actions = {
            "1": cls.Toggle,
            "2": cls.Restart,
            "3": cls.ViewStatus,
            "4": cls.ViewClients,
            "5": cls.OpenSettings,
        }

        action = actions.get(choice)

        if action is None:
            Message.Render(
                text="Invalid choice. Please enter a number from the menu.",
                kind="error",
            )
            return

        action(manager)

    # Shows a success or error message on Screen 2.
    @classmethod
    def ShowResult(cls, success: bool, message: str) -> None:
        kind = "success" if success else "error"
        Message.Render(text=message, kind=kind)

    # Action: toggle server between running and stopped.
    @classmethod
    def Toggle(cls, manager: Manager) -> None:
        if manager.IsActive():
            success, message = manager.Stop()
        else:
            success, message = manager.Start()

        cls.ShowResult(success, message)

    # Action: restart the server.
    @classmethod
    def Restart(cls, manager: Manager) -> None:
        success, message = manager.Restart()
        cls.ShowResult(success, message)

    # Action: show detailed status on Screen 3.
    @classmethod
    def ViewStatus(cls, manager: Manager) -> None:
        status = manager.Status()

        Detail.Render(
            title="Server Status",
            rows=[
                ("State:", "Running" if status["active"] else "Stopped"),
                ("Host:", status["host"]),
                ("Port:", str(status["port"])),
                ("Uptime:", Panel.FormatUptime(status["uptime"])),
                ("Clients:", str(status["clients"])),
            ],
        )

    # Action: list connected clients on Screen 3.
    @classmethod
    def ViewClients(cls, manager: Manager) -> None:
        if not manager.IsActive():
            Message.Render(text="Server is not running.", kind="error")
            return

        clients = manager.Clients()
        items = [
            f"{client['address']}  [{client['role_label']}]"
            for client in clients
        ]
        Detail.RenderList(
            title="Connected Clients",
            items=items,
            empty="No clients connected.",
        )

    # Action: open the settings hub submenu.
    @classmethod
    def OpenSettings(cls, manager: Manager) -> None:
        Hub.Run(manager)

    # Action: exit the panel and shut down the server.
    @classmethod
    def Exit(cls, manager: Manager) -> None:
        if manager.IsActive():
            manager.Stop()

        Panel.Clear()
        Message.Render(text="Goodbye! Server has been shut down.", kind="info")
