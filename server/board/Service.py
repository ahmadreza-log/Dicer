from board.Settings import Settings as Panel
from config.Settings import ResolveHost
from config.Settings import Settings as Network
from config.Store import Store
from connection.Settings import Settings as Connection
from database.Engine import Engine
from database.Settings import Settings as Database
from logger.Logger import Logger
from logger.Settings import Settings as Logging
from security.Settings import Settings as Security


class Service:
    # Applies settings changes from the Dash panel with CLI-equivalent side effects.

    @staticmethod
    def ParseInt(value) -> int | None:
        # Dash number inputs often return float (e.g. 1050.0), not int strings.
        if value is None or value == "":
            return None

        try:
            return int(float(value))
        except (TypeError, ValueError):
            return None

    @classmethod
    def Persist(cls) -> tuple[bool, str]:
        return Store.Save()

    @classmethod
    def Commit(cls, success: bool, message: str) -> tuple[bool, str]:
        if not success:
            return False, message

        saved, save_message = cls.Persist()

        if saved:
            return True, f"{message} Saved to {Store.Filename}."

        return False, f"{message} Could not save to disk: {save_message}"

    @classmethod
    def RestartIfActive(cls, manager) -> tuple[bool, str]:
        if manager is None:
            return True, ""

        return manager.ReloadIfActive()

    @classmethod
    def WithRestart(cls, manager, message: str) -> tuple[bool, str]:
        restart_ok, restart_message = cls.RestartIfActive(manager)

        if not restart_message:
            return True, message

        if restart_ok:
            bind = ResolveHost()
            return True, f"{message} Server restarted on {bind}:{Network.Port}."

        return False, f"{message} Server restart failed: {restart_message}"

    @classmethod
    def Log(cls, bridge, message: str, kind: str = "info") -> None:
        bridge.Log(message, kind)
        bridge.Notify(message)

    @classmethod
    def ApplyNetwork(
        cls,
        manager,
        host: str,
        mode: str,
        max_clients: str,
        auto_start: bool,
    ) -> tuple[bool, str]:
        errors = cls.ValidateNetwork(host, mode, max_clients)

        if errors:
            return False, errors

        max_value = cls.ParseInt(max_clients)

        if max_value is None:
            return False, "Max clients must be a valid number."

        reload = host != Network.Host or mode != Network.Mode

        Network.Host = host.strip()
        Network.Mode = mode
        Network.MaxClients = max_value
        Network.AutoStart = auto_start

        if mode == "Custom" and not Network.Host:
            return False, "Host is required in Custom mode."

        saved, save_message = cls.Persist()

        if not saved:
            return False, save_message

        label = str(max_value) if max_value > 0 else "unlimited"

        if reload:
            success, message = manager.ReloadAfterNetworkChange()
            bind = ResolveHost()

            if success:
                text = f"Network updated. Bind: {bind}:{Network.Port}. {message} Saved to {Store.Filename}."
                return True, text

            return False, f"Network saved but restart failed: {message}"

        return True, f"Network settings saved. Max clients: {label}. Saved to {Store.Filename}."

    @classmethod
    def ValidateNetwork(
        cls,
        host: str,
        mode: str,
        max_clients: str,
    ) -> str:
        if mode not in ("Local", "Network", "Custom"):
            return "Invalid listen mode."

        if mode == "Custom" and not str(host).strip():
            return "Host cannot be empty in Custom mode."

        max_value = cls.ParseInt(max_clients)

        if max_value is None:
            return "Max clients must be a number."

        if max_value < 0:
            return "Max clients cannot be negative."

        return ""

    @classmethod
    def ApplyLogging(
        cls,
        enabled: bool,
        level: str,
        console: bool,
        file: bool,
        directory: str,
        filename: str,
        max_mb: str,
        backups: str,
    ) -> tuple[bool, str]:
        if level.upper() not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            return False, "Invalid log level."

        if not str(directory).strip():
            return False, "Log directory cannot be empty."

        if not str(filename).strip():
            return False, "Log filename cannot be empty."

        size_value = cls.ParseInt(max_mb)
        backup_value = cls.ParseInt(backups)

        if size_value is None or size_value < 1:
            return False, "Max file size must be at least 1 MB."

        if backup_value is None or backup_value < 0:
            return False, "Backup count must be zero or greater."

        Logging.Enabled = enabled
        Logging.Level = level.upper()
        Logging.Console = console
        Logging.File = file
        Logging.Directory = directory.strip()
        Logging.Filename = filename.strip()
        Logging.MaxBytes = size_value * 1024 * 1024
        Logging.Backups = backup_value
        Logger.Reset()

        state = "enabled" if enabled else "disabled"
        return cls.Commit(True, f"Logging {state} at {Logging.Level} level.")

    @classmethod
    def ApplyConnection(
        cls,
        manager,
        welcome: str,
        buffer: str,
        timeout: str,
        max_per: str,
    ) -> tuple[bool, str]:
        if not str(welcome).strip():
            return False, "Welcome message cannot be empty."

        buffer_value = cls.ParseInt(buffer)
        timeout_value = cls.ParseInt(timeout)
        max_value = cls.ParseInt(max_per)

        if buffer_value is None or buffer_value < 256:
            return False, "Buffer must be at least 256 bytes."

        if timeout_value is None or timeout_value < 0:
            return False, "Timeout must be zero or greater."

        if max_value is None or max_value < 0:
            return False, "Max per address must be zero or greater."

        Connection.Welcome = welcome.strip()
        Connection.Buffer = buffer_value
        Connection.Timeout = timeout_value
        Connection.MaxPerAddress = max_value

        saved, save_message = cls.Persist()

        if not saved:
            return False, save_message

        success, message = cls.WithRestart(manager, "Connection settings saved.")

        if not success:
            return False, f"{message} Saved to {Store.Filename}."

        return True, f"{message} Saved to {Store.Filename}."

    @classmethod
    def ApplySecurity(
        cls,
        password: str,
        allowed: str,
        blocked: str,
    ) -> tuple[bool, str]:
        Security.Password = password or ""
        Security.Allowed = allowed.strip()
        Security.Blocked = blocked.strip()

        mode = "password protected" if Security.Password else "open"
        return cls.Commit(True, f"Security settings saved. Mode: {mode}.")

    @classmethod
    def ApplyDatabase(
        cls,
        manager,
        enabled: bool,
        host: str,
        port: str,
        user: str,
        password: str,
        name: str,
    ) -> tuple[bool, str]:
        if not str(host).strip():
            return False, "Database host cannot be empty."

        port_value = cls.ParseInt(port)

        if port_value is None:
            return False, "Database port must be a number."

        if port_value < 1 or port_value > 65535:
            return False, "Database port must be between 1 and 65535."

        if not str(user).strip():
            return False, "Database user cannot be empty."

        if not str(name).strip():
            return False, "Database name cannot be empty."

        was_enabled = Database.Enabled
        previous = {
            "enabled": was_enabled,
            "host": Database.Host,
            "port": Database.Port,
            "user": Database.User,
            "password": Database.Password,
            "name": Database.Name,
        }

        Database.Enabled = enabled
        Database.Host = host.strip()
        Database.Port = port_value
        Database.User = user.strip()
        Database.Password = password or ""
        Database.Name = name.strip()

        saved, save_message = cls.Persist()

        if not saved:
            return False, save_message

        if enabled and not was_enabled:
            success, message = Engine.ConnectDirect()

            if not success:
                Database.Enabled = False
                cls.Persist()
                return False, message
        elif not enabled and Engine.IsActive():
            Engine.Disconnect()
            success, message = True, "Database disabled and disconnected."
        elif enabled:
            success, message = Engine.Reload()

            if not success:
                return False, message
        else:
            success, message = True, "Database settings saved."

        changed = (
            previous["host"] != Database.Host
            or previous["port"] != Database.Port
            or previous["user"] != Database.User
            or previous["password"] != Database.Password
            or previous["name"] != Database.Name
            or previous["enabled"] != Database.Enabled
        )

        if changed and success:
            restart_ok, restart_message = cls.RestartIfActive(manager)

            if restart_message:
                if restart_ok:
                    bind = ResolveHost()
                    message = (
                        f"{message} Server restarted on {bind}:{Network.Port}."
                    )
                else:
                    return False, f"{message} Server restart failed: {restart_message}"

        return True, f"{message} Saved to {Store.Filename}."

    @classmethod
    def ApplyPanel(
        cls,
        host: str,
        port: str,
        interval: str,
        debug: bool,
    ) -> tuple[bool, str, int]:
        if not str(host or "").strip():
            return False, "Dashboard host cannot be empty.", Panel.Interval

        port_value = cls.ParseInt(port)
        seconds = cls.ParseInt(interval)

        if port_value is None:
            return False, "Dashboard port must be a number.", Panel.Interval

        if port_value < 1 or port_value > 65535:
            return False, "Dashboard port must be between 1 and 65535.", Panel.Interval

        if seconds is None or seconds < 1:
            return False, "Refresh interval must be at least 1 second.", Panel.Interval

        milliseconds = seconds * 1000

        Panel.Host = host.strip()
        Panel.Port = port_value
        Panel.Interval = milliseconds
        Panel.Debug = debug

        cls.Persist()

        message = (
            f"Panel settings applied. Live refresh every {seconds}s. "
            f"Restart --dash only if you changed host or port."
        )

        return True, message, Panel.Interval

    @classmethod
    def TestDatabase(cls) -> tuple[bool, str]:
        return Engine.Test()

    @classmethod
    def ConnectDatabase(cls) -> tuple[bool, str]:
        success, message = Engine.ConnectDirect()

        if success:
            Database.Enabled = True
            return cls.Commit(True, message)

        return False, message

    @classmethod
    def DisconnectDatabase(cls) -> tuple[bool, str]:
        Engine.Disconnect()
        Database.Enabled = False
        return cls.Commit(True, "Database disconnected.")

    @classmethod
    def Save(cls) -> tuple[bool, str]:
        return Store.Save()

    @classmethod
    def Load(cls, manager) -> tuple[bool, str]:
        if manager.IsActive():
            return False, "Stop the server before loading settings."

        success, message = Store.Load()

        if success:
            Engine.Reload()

        return success, message

    @classmethod
    def Reset(cls, manager) -> tuple[bool, str]:
        if manager.IsActive():
            return False, "Stop the server before resetting settings."

        success, message = Store.Reset()

        if success:
            Engine.Disconnect()

        return success, message
