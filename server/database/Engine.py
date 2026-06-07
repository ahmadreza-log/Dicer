from database.Base import Base
from database.Settings import Settings


class Engine:
    # Database engine facade that selects the correct driver by Type.
    # Currently supports MySQL; more drivers can be registered later.

    driver: Base | None = None

    # Creates a driver instance based on the configured engine type.
    @classmethod
    def Create(cls) -> Base:
        if Settings.Type == "MySQL":
            from database.mysql.Driver import Driver

            return Driver()

        from database.mysql.Driver import Driver

        return Driver()

    # Connects to the database when enabled in settings.
    @classmethod
    def Connect(cls) -> tuple[bool, str]:
        if not Settings.Enabled:
            return False, "Database is disabled in settings."

        return cls.ConnectDirect()

    # Connects directly without checking the Enabled flag.
    @classmethod
    def ConnectDirect(cls) -> tuple[bool, str]:
        cls.Disconnect()
        cls.driver = cls.Create()
        success, message = cls.driver.Connect()

        if success:
            cls._Prepare()

        return success, message

    # Disconnects from the database and releases the driver.
    @classmethod
    def Disconnect(cls) -> None:
        if cls.driver is not None:
            cls.driver.Disconnect()

        cls.driver = None

    # Ensures campaign tables exist after a successful connection.
    @classmethod
    def _Prepare(cls) -> None:
        if not cls.IsActive():
            return

        from database.campaigns.Repository import Repository as Campaigns

        Campaigns.Ensure()

    # Tests the connection without keeping it open (works even when disabled).
    @classmethod
    def Test(cls) -> tuple[bool, str]:
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
            return True, "Settings updated."

        if was_active:
            return cls.ConnectDirect()

        return True, "Settings updated."
