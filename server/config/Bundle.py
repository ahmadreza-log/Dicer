from board.Settings import Settings as Panel
from config.Settings import Settings as Network
from connection.Settings import Settings as Connection
from database.Settings import Settings as Database
from logger.Settings import Settings as Logger
from security.Settings import Settings as Security


class Bundle:
    # Aggregates every settings group into a single snapshot for save/load.

    Defaults = {
        "network": {
            "Host": "127.0.0.1",
            "Mode": "Local",
            "MaxClients": 0,
            "AutoStart": True,
        },
        "logging": {
            "Enabled": False,
            "Level": "INFO",
            "Directory": "logs",
            "Filename": "dicer.log",
            "MaxBytes": 5242880,
            "Backups": 5,
            "Console": True,
            "File": True,
        },
        "connection": {
            "Welcome": "Connected to Dicer server",
            "Buffer": 4096,
            "Timeout": 0,
            "MaxPerAddress": 0,
        },
        "security": {
            "Password": "",
            "Allowed": "",
            "Blocked": "",
        },
        "database": {
            "Enabled": False,
            "Type": "MySQL",
            "Host": "127.0.0.1",
            "Port": 3306,
            "User": "root",
            "Password": "",
            "Name": "dicer",
        },
        "panel": {
            "Host": "127.0.0.1",
            "Port": 8050,
            "Debug": False,
            "Interval": 2000,
        },
    }

    # Captures all current settings as a dictionary.
    @staticmethod
    def Snapshot() -> dict:
        return {
            "network": {
                "Host": Network.Host,
                "Mode": Network.Mode,
                "MaxClients": Network.MaxClients,
                "AutoStart": Network.AutoStart,
            },
            "logging": {
                "Enabled": Logger.Enabled,
                "Level": Logger.Level,
                "Directory": Logger.Directory,
                "Filename": Logger.Filename,
                "MaxBytes": Logger.MaxBytes,
                "Backups": Logger.Backups,
                "Console": Logger.Console,
                "File": Logger.File,
            },
            "connection": {
                "Welcome": Connection.Welcome,
                "Buffer": Connection.Buffer,
                "Timeout": Connection.Timeout,
                "MaxPerAddress": Connection.MaxPerAddress,
            },
            "security": {
                "Password": Security.Password,
                "Allowed": Security.Allowed,
                "Blocked": Security.Blocked,
            },
            "database": {
                "Enabled": Database.Enabled,
                "Type": Database.Type,
                "Host": Database.Host,
                "Port": Database.Port,
                "User": Database.User,
                "Password": Database.Password,
                "Name": Database.Name,
            },
            "panel": {
                "Host": Panel.Host,
                "Port": Panel.Port,
                "Debug": Panel.Debug,
                "Interval": Panel.Interval,
            },
        }

    # Applies a saved dictionary to all settings modules.
    @staticmethod
    def Apply(data: dict) -> None:
        network = data.get("network", {})
        Network.Host = network.get("Host", Network.Host)
        Network.Mode = network.get("Mode", Network.Mode)
        Network.MaxClients = int(network.get("MaxClients", Network.MaxClients))
        Network.AutoStart = bool(network.get("AutoStart", Network.AutoStart))

        logging = data.get("logging", {})
        Logger.Enabled = bool(logging.get("Enabled", Logger.Enabled))
        Logger.Level = logging.get("Level", Logger.Level)
        Logger.Directory = logging.get("Directory", Logger.Directory)
        Logger.Filename = logging.get("Filename", Logger.Filename)
        Logger.MaxBytes = int(logging.get("MaxBytes", Logger.MaxBytes))
        Logger.Backups = int(logging.get("Backups", Logger.Backups))
        Logger.Console = bool(logging.get("Console", Logger.Console))
        Logger.File = bool(logging.get("File", Logger.File))

        connection = data.get("connection", {})
        Connection.Welcome = connection.get("Welcome", Connection.Welcome)
        Connection.Buffer = int(connection.get("Buffer", Connection.Buffer))
        Connection.Timeout = int(connection.get("Timeout", Connection.Timeout))
        Connection.MaxPerAddress = int(
            connection.get("MaxPerAddress", Connection.MaxPerAddress)
        )

        security = data.get("security", {})
        Security.Password = security.get("Password", Security.Password)
        Security.Allowed = security.get("Allowed", Security.Allowed)
        Security.Blocked = security.get("Blocked", Security.Blocked)

        database = data.get("database", {})
        Database.Enabled = bool(database.get("Enabled", Database.Enabled))
        Database.Type = database.get("Type", Database.Type)
        Database.Host = database.get("Host", Database.Host)
        Database.Port = int(database.get("Port", Database.Port))
        Database.User = database.get("User", Database.User)
        Database.Password = database.get("Password", Database.Password)
        Database.Name = database.get("Name", Database.Name)

        panel = data.get("panel", {})
        Panel.Host = panel.get("Host", Panel.Host)
        Panel.Port = int(panel.get("Port", Panel.Port))
        Panel.Debug = bool(panel.get("Debug", Panel.Debug))
        Panel.Interval = int(panel.get("Interval", Panel.Interval))

    # Restores every setting to its factory default value.
    @staticmethod
    def Reset() -> None:
        Bundle.Apply(Bundle.Defaults)
