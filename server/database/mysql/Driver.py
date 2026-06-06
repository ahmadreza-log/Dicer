from database.Base import Base
from database.Settings import Settings


class Driver(Base):
    # MySQL database driver using mysql-connector-python.

    def __init__(self) -> None:
        self.link = None

    # Loads the MySQL connector or returns a clear install message.
    @staticmethod
    def LoadConnector():
        try:
            import mysql.connector
            from mysql.connector import Error

            return mysql.connector, Error
        except ImportError:
            return None, None

    # Opens a connection to the configured MySQL server.
    def Connect(self) -> tuple[bool, str]:
        connector, error_type = self.LoadConnector()

        if connector is None:
            return False, (
                "mysql-connector-python is not installed. "
                "Run: pip install -r requirements.txt"
            )

        try:
            self.link = connector.connect(
                host=Settings.Host,
                port=Settings.Port,
                user=Settings.User,
                password=Settings.Password,
                database=Settings.Name,
            )
            return True, (
                f"Connected to MySQL at {Settings.Host}:{Settings.Port}/{Settings.Name}"
            )
        except error_type as error:
            self.link = None
            return False, f"MySQL connection failed. Reason: {error}"

    # Closes the active MySQL connection if one exists.
    def Disconnect(self) -> None:
        if self.link is not None and self.link.is_connected():
            self.link.close()

        self.link = None

    # Verifies server access and whether the configured database exists.
    def Test(self) -> tuple[bool, str]:
        connector, error_type = self.LoadConnector()

        if connector is None:
            return False, (
                "mysql-connector-python is not installed. "
                "Run: pip install -r requirements.txt"
            )

        try:
            link = connector.connect(
                host=Settings.Host,
                port=Settings.Port,
                user=Settings.User,
                password=Settings.Password,
            )
            cursor = link.cursor()
            cursor.execute(
                "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s",
                (Settings.Name,),
            )
            exists = cursor.fetchone() is not None
            cursor.close()
            link.close()

            if not exists:
                return False, (
                    f"Server reachable but database '{Settings.Name}' does not exist. "
                    f"Create it in MySQL first."
                )

            return True, (
                f"MySQL OK at {Settings.Host}:{Settings.Port}/{Settings.Name}"
            )
        except error_type as error:
            return False, f"MySQL test failed. Reason: {error}"

    # Returns whether a live MySQL connection is currently open.
    def IsActive(self) -> bool:
        return self.link is not None and self.link.is_connected()
