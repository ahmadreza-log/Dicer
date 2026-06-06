import mysql.connector
from mysql.connector import Error

from database.Base import Base
from database.Settings import Settings


class Driver(Base):
    # MySQL database driver using mysql-connector-python.

    def __init__(self) -> None:
        self.link = None

    # Opens a connection to the configured MySQL server.
    def Connect(self) -> tuple[bool, str]:
        try:
            self.link = mysql.connector.connect(
                host=Settings.Host,
                port=Settings.Port,
                user=Settings.User,
                password=Settings.Password,
                database=Settings.Name,
            )
            return True, (
                f"Connected to MySQL at {Settings.Host}:{Settings.Port}/{Settings.Name}"
            )
        except Error as error:
            self.link = None
            return False, f"MySQL connection failed. Reason: {error}"

    # Closes the active MySQL connection if one exists.
    def Disconnect(self) -> None:
        if self.link is not None and self.link.is_connected():
            self.link.close()

        self.link = None

    # Connects briefly to verify credentials and database availability.
    def Test(self) -> tuple[bool, str]:
        success, message = self.Connect()

        if success:
            self.Disconnect()

        return success, message

    # Returns whether a live MySQL connection is currently open.
    def IsActive(self) -> bool:
        return self.link is not None and self.link.is_connected()
