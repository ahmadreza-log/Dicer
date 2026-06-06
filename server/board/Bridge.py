from datetime import datetime

from cli.Manager import Manager
from database.Engine import Engine
from database.Settings import Settings as Database


class Bridge:
    # Shared bridge between Dash callbacks and server/database managers.

    manager: Manager | None = None
    history: list[dict] = []
    limit = 60
    alert = ""
    activities: list[dict] = []

    # Attaches the active server manager instance.
    @classmethod
    def Attach(cls, manager: Manager) -> None:
        cls.manager = manager

    # Returns current TCP server status from the manager.
    @classmethod
    def Status(cls) -> dict:
        if cls.manager is None:
            return {
                "active": False,
                "host": "—",
                "port": 0,
                "uptime": 0,
                "clients": 0,
            }

        return cls.manager.Status()

    # Returns connected client address strings.
    @classmethod
    def Clients(cls) -> list[str]:
        if cls.manager is None:
            return []

        return cls.manager.Clients()

    # Records a client-count sample for the live chart.
    @classmethod
    def Record(cls) -> None:
        status = cls.Status()
        point = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "clients": status["clients"],
        }
        cls.history.append(point)

        if len(cls.history) > cls.limit:
            cls.history.pop(0)

    # Returns database connection summary for the dashboard.
    @classmethod
    def Database(cls) -> dict:
        return {
            "enabled": Database.Enabled,
            "active": Engine.IsActive(),
            "host": Database.Host,
            "port": Database.Port,
            "user": Database.User,
            "name": Database.Name,
        }

    # Stores the latest user-facing alert message.
    @classmethod
    def Notify(cls, message: str) -> str:
        cls.alert = message
        return message

    # Appends an entry to the recent activity feed.
    @classmethod
    def Log(cls, message: str, kind: str = "info") -> None:
        entry = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "message": message,
            "kind": kind,
        }
        cls.activities.insert(0, entry)

        if len(cls.activities) > 20:
            cls.activities.pop()

    # Cleans up server and database on dashboard shutdown.
    @classmethod
    def Cleanup(cls) -> None:
        if cls.manager is not None:
            cls.manager.Cleanup()

        if Database.Enabled or Engine.IsActive():
            Engine.Disconnect()
