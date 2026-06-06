from cli.Manager import Manager
from cli.Panel import Panel


class Main:
    # Screen 1 — main menu with server status and action list.

    @classmethod
    def Render(cls, manager: Manager) -> None:
        Panel.Clear()
        Panel.Banner()
        cls.Status(manager.Status())
        cls.Options(manager)

    # Prints the compact status line at the top of the main screen.
    @classmethod
    def Status(cls, status: dict) -> None:
        if status["active"]:
            state = "🟢 Running"
            uptime = Panel.FormatUptime(status["uptime"])
            extra = f" | Uptime: {uptime} | Clients: {status['clients']}"
        else:
            state = "🔴 Stopped"
            extra = ""

        print(f"  Status: {state} | Host: {status['host']} | Port: {status['port']}{extra}")
        print()

    # Prints numbered menu options with a dynamic Start/Stop toggle label.
    @classmethod
    def Options(cls, manager: Manager) -> None:
        if manager.IsActive():
            toggle = "⏹️  Stop Server"
        else:
            toggle = "▶️  Start Server"

        options = [
            ("1", toggle),
            ("2", "🔄  Restart Server"),
            ("3", "📊  View Status"),
            ("4", "👥  View Connected Clients"),
            ("5", "⚙️  Settings"),
            ("0", "❌  Exit"),
        ]

        for number, label in options:
            print(f"  [{number}] {label}")

        print()
