from config.Settings import ResolveHost
from config.Settings import Settings as NetworkSettings
from config.Store import Store
from connection.Settings import Settings as ConnectionSettings
from logger.Settings import Settings as LoggerSettings
from security.Settings import Settings as SecuritySettings
from cli.Manager import Manager


class Summary:
    # Builds compact setting summaries shown on each settings screen.

    @staticmethod
    def FormatBool(value: bool) -> str:
        return "Yes" if value else "No"

    @staticmethod
    def FormatLimit(value: int, suffix: str = "") -> str:
        if value <= 0:
            return "Unlimited"

        return f"{value}{suffix}"

    @staticmethod
    def Clip(text: str, length: int = 28) -> str:
        if len(text) <= length:
            return text

        return f"{text[: length - 3]}..."

    @classmethod
    def Lines(cls, rows: list[tuple[str, str]]) -> list[str]:
        return [f"{label:<14} {value}" for label, value in rows]

    @classmethod
    def Network(cls) -> list[str]:
        return cls.Lines([
            ("Host:", NetworkSettings.Host),
            ("Port:", str(NetworkSettings.Port)),
            ("Mode:", NetworkSettings.Mode),
            ("Bind:", ResolveHost()),
            ("Max Clients:", cls.FormatLimit(NetworkSettings.MaxClients)),
            ("Auto Start:", cls.FormatBool(NetworkSettings.AutoStart)),
        ])

    @classmethod
    def Logging(cls) -> list[str]:
        return cls.Lines([
            ("Enabled:", cls.FormatBool(LoggerSettings.Enabled)),
            ("Level:", LoggerSettings.Level),
            ("Console:", cls.FormatBool(LoggerSettings.Console)),
            ("File:", cls.FormatBool(LoggerSettings.File)),
            ("Directory:", LoggerSettings.Directory),
            ("Max Size:", f"{LoggerSettings.MaxBytes // (1024 * 1024)} MB"),
            ("Backups:", str(LoggerSettings.Backups)),
        ])

    @classmethod
    def Connection(cls) -> list[str]:
        return cls.Lines([
            ("Welcome:", cls.Clip(ConnectionSettings.Welcome)),
            ("Buffer:", f"{ConnectionSettings.Buffer} bytes"),
            ("Timeout:", cls.FormatLimit(ConnectionSettings.Timeout, "s")),
            ("Max / IP:", cls.FormatLimit(ConnectionSettings.MaxPerAddress)),
        ])

    @classmethod
    def Security(cls) -> list[str]:
        allowed = SecuritySettings.Allowed or "All"
        blocked = SecuritySettings.Blocked or "None"

        return cls.Lines([
            ("Password:", "Set" if SecuritySettings.Password else "None"),
            ("Allowed:", cls.Clip(allowed, 32)),
            ("Blocked:", cls.Clip(blocked, 32)),
        ])

    @classmethod
    def Persist(cls) -> list[str]:
        exists = "Yes" if Store.Path().exists() else "No"

        return cls.Lines([
            ("File:", Store.Filename),
            ("Saved:", exists),
            ("Location:", "config/"),
        ])

    @classmethod
    def All(cls, manager: Manager) -> list[str]:
        status = manager.Status()
        state = "Running" if status["active"] else "Stopped"

        return cls.Lines([
            ("Network:", f"{ResolveHost()}:{NetworkSettings.Port}"),
            ("Mode:", NetworkSettings.Mode),
            ("Logging:", "On" if LoggerSettings.Enabled else "Off"),
            ("Level:", LoggerSettings.Level),
            ("Welcome:", cls.Clip(ConnectionSettings.Welcome, 22)),
            ("Security:", "Password" if SecuritySettings.Password else "Open"),
            ("Store:", "Saved" if Store.Path().exists() else "Not saved"),
            ("Server:", f"{state} | {status['clients']} clients"),
        ])

    @classmethod
    def AllRows(cls, manager: Manager) -> list[tuple[str, str]]:
        status = manager.Status()
        bind = ResolveHost()

        return [
            ("── Network ──", ""),
            ("Host:", NetworkSettings.Host),
            ("Port:", str(NetworkSettings.Port)),
            ("Mode:", NetworkSettings.Mode),
            ("Bind:", bind),
            ("Max Clients:", cls.FormatLimit(NetworkSettings.MaxClients)),
            ("Auto Start:", cls.FormatBool(NetworkSettings.AutoStart)),
            ("── Logging ──", ""),
            ("Enabled:", cls.FormatBool(LoggerSettings.Enabled)),
            ("Level:", LoggerSettings.Level),
            ("Console:", cls.FormatBool(LoggerSettings.Console)),
            ("File:", cls.FormatBool(LoggerSettings.File)),
            ("Directory:", LoggerSettings.Directory),
            ("Max Size:", f"{LoggerSettings.MaxBytes // (1024 * 1024)} MB"),
            ("Backups:", str(LoggerSettings.Backups)),
            ("── Connection ──", ""),
            ("Welcome:", cls.Clip(ConnectionSettings.Welcome, 32)),
            ("Buffer:", str(ConnectionSettings.Buffer)),
            ("Timeout:", cls.FormatLimit(ConnectionSettings.Timeout, "s")),
            ("Max / IP:", cls.FormatLimit(ConnectionSettings.MaxPerAddress)),
            ("── Security ──", ""),
            ("Password:", "Set" if SecuritySettings.Password else "None"),
            ("Allowed:", SecuritySettings.Allowed or "All"),
            ("Blocked:", SecuritySettings.Blocked or "None"),
            ("── Storage ──", ""),
            ("File:", Store.Filename),
            ("Saved:", cls.FormatBool(Store.Path().exists())),
            ("── Runtime ──", ""),
            ("State:", "Running" if status["active"] else "Stopped"),
            ("Clients:", str(status["clients"])),
        ]
