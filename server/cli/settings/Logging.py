from logger.Logger import Logger
from logger.Settings import Settings
from cli.Manager import Manager
from cli.screens.Message import Message
from cli.screens.Prompt import Prompt
from cli.screens.Submenu import Submenu
from cli.settings.Input import Input
from cli.settings.Summary import Summary


class Logging:
    # Logging settings submenu.

    Options = [
        ("1", "📊  Enable Logging"),
        ("2", "📶  Log Level"),
        ("3", "🖥️  Console Output"),
        ("4", "💾  File Output"),
        ("5", "📁  Log Directory"),
        ("6", "📦  Max File Size (MB)"),
        ("7", "🗂️  Backup Count"),
    ]

    @classmethod
    def Run(cls, manager: Manager) -> None:
        while True:
            Submenu.Render("Logging Settings", cls.Options, Summary.Logging())
            choice = Submenu.Read()

            if choice == "0":
                return

            actions = {
                "1": cls.ToggleEnabled,
                "2": cls.ChangeLevel,
                "3": cls.ToggleConsole,
                "4": cls.ToggleFile,
                "5": cls.ChangeDirectory,
                "6": cls.ChangeMaxBytes,
                "7": cls.ChangeBackups,
            }

            action = actions.get(choice)

            if action is None:
                Message.Render(text="Invalid choice.", kind="error")
                continue

            action(manager)

    @classmethod
    def ApplyLogger(cls) -> None:
        Logger.Reset()

    @classmethod
    def ToggleEnabled(cls, manager: Manager) -> None:
        Settings.Enabled = Input.Toggle("Logging", Settings.Enabled)
        cls.ApplyLogger()
        state = "enabled" if Settings.Enabled else "disabled"
        Message.Render(text=f"Logging {state}.", kind="success")

    @classmethod
    def ChangeLevel(cls, manager: Manager) -> None:
        raw = Prompt.Ask(
            title="Log Level",
            rows=[
                ("Current:", Settings.Level),
                ("", "DEBUG, INFO, WARNING, ERROR, CRITICAL"),
            ],
            label="New level",
        ).upper()

        valid = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

        if raw not in valid:
            Message.Render(text="Invalid log level.", kind="error")
            return

        Settings.Level = raw
        cls.ApplyLogger()
        Message.Render(text=f"Log level set to {raw}.", kind="success")

    @classmethod
    def ToggleConsole(cls, manager: Manager) -> None:
        Settings.Console = Input.Toggle("Console Output", Settings.Console)
        cls.ApplyLogger()
        Message.Render(text="Console output updated.", kind="success")

    @classmethod
    def ToggleFile(cls, manager: Manager) -> None:
        Settings.File = Input.Toggle("File Output", Settings.File)
        cls.ApplyLogger()
        Message.Render(text="File output updated.", kind="success")

    @classmethod
    def ChangeDirectory(cls, manager: Manager) -> None:
        directory = Prompt.Ask(
            title="Log Directory",
            rows=[("Current:", Settings.Directory)],
            label="New directory",
        )

        if not directory:
            Message.Render(text="Directory cannot be empty.", kind="error")
            return

        Settings.Directory = directory
        cls.ApplyLogger()
        Message.Render(text=f"Log directory set to {directory}.", kind="success")

    @classmethod
    def ChangeMaxBytes(cls, manager: Manager) -> None:
        current = Settings.MaxBytes // (1024 * 1024)
        raw = Prompt.Ask(
            title="Max File Size",
            rows=[("Current (MB):", str(current))],
            label="New size (MB)",
        )

        if not raw.isdigit() or int(raw) < 1:
            Message.Render(text="Size must be a positive number.", kind="error")
            return

        Settings.MaxBytes = int(raw) * 1024 * 1024
        cls.ApplyLogger()
        Message.Render(text=f"Max file size set to {raw} MB.", kind="success")

    @classmethod
    def ChangeBackups(cls, manager: Manager) -> None:
        raw = Prompt.Ask(
            title="Backup Count",
            rows=[("Current:", str(Settings.Backups))],
            label="New count",
        )

        if not raw.isdigit():
            Message.Render(text="Count must be a number.", kind="error")
            return

        Settings.Backups = int(raw)
        cls.ApplyLogger()
        Message.Render(text=f"Backup count set to {raw}.", kind="success")
