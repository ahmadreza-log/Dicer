from database.Base import Base
from database.Settings import Settings
from database.mysql.Driver import Driver as MysqlDriver


class Engine:
    # Database engine facade that selects the correct driver by Type.
    # Currently supports MySQL; more drivers can be registered later.

    driver: Base | None = None

    # Creates a driver instance based on the configured engine type.
    @classmethod
    def Create(cls) -> Base:
        if Settings.Type == "MySQL":
            return MysqlDriver()

        return MysqlDriver()

    # Connects to the database when enabled in settings.
    @classmethod
    def Connect(cls) -> tuple[bool, str]:
        if not Settings.Enabled:
            return False, "Database is disabled in settings."

        cls.Disconnect()
        cls.driver = cls.Create()
        return cls.driver.Connect()

    # Disconnects from the database and releases the driver.
    @classmethod
    def Disconnect(cls) -> None:
        if cls.driver is not None:
            cls.driver.Disconnect()

        cls.driver = None

    # Tests the connection without keeping it open.
    @classmethod
    def Test(cls) -> tuple[bool, str]:
        if not Settings.Enabled:
            return False, "Enable the database in settings before testing."

        tester = cls.Create()
        return tester.Test()

    # Returns whether the engine currently holds an active connection.
    @classmethod
    def IsActive(cls) -> bool:
        return cls.driver is not None and cls.driver.IsActive()

    # Reconnects after settings change if the database was previously active.
    @classmethod
    def Reload(cls) -> tuple[bool, str]:
        was_active = cls.IsActive()
        cls.Disconnect()

        if not Settings.Enabled:
            return True, "Database disabled."

        if was_active:
            return cls.Connect()

        return True, "Settings updated."
