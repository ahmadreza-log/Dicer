import time

from config.Settings import ResolveHost
from config.Settings import Settings as Network
from network.Server import Server


class Manager:
    # Controls server lifecycle from the interactive CLI panel.

    def __init__(self) -> None:
        self.server: Server | None = None

    @property
    def host(self) -> str:
        return ResolveHost()

    @property
    def port(self) -> int:
        return Network.Port

    # Returns True when the server accept loop is active.
    def IsActive(self) -> bool:
        return self.server is not None and self.server.IsRunning()

    # Starts the server on a background thread.
    def Start(self) -> tuple[bool, str]:
        if self.IsActive():
            return False, "Server is already running."

        self.server = Server(host=self.host, port=self.port)
        self.server.Launch()
        time.sleep(0.3)

        if self.IsActive():
            return True, f"Server started on {self.host}:{self.port}"

        reason = self.server.reason or "Unknown error"
        self.server = None
        return False, f"Could not start server. Reason: {reason}"

    # Stops the running server and disconnects all clients.
    def Stop(self) -> tuple[bool, str]:
        if not self.IsActive():
            return False, "Server is not running."

        self.server.Stop()
        self.server = None
        return True, "Server stopped."

    # Restarts the server with current settings.
    def Restart(self) -> tuple[bool, str]:
        if self.IsActive():
            self.server.Stop()
            self.server = None
            time.sleep(0.5)

        return self.Start()

    # Restarts the server when it is running; no-op when already stopped.
    def ReloadIfActive(self) -> tuple[bool, str]:
        if not self.IsActive():
            return True, ""

        return self.Restart()

    # Stops the server, applies network setting changes, and restarts if it was running.
    def ReloadAfterNetworkChange(self) -> tuple[bool, str]:
        was_active = self.IsActive()

        if was_active:
            self.server.Stop()
            self.server = None
            time.sleep(0.5)

        if was_active:
            success, message = self.Start()

            if success:
                return True, f"Server restarted on {self.host}:{self.port}"

            return False, message

        return True, "Settings updated."

    # Returns a dictionary of current server status details.
    def Status(self) -> dict:
        active = self.IsActive()
        uptime = self.server.Uptime() if active else 0
        clients = self.server.Clients() if active else 0

        return {
            "active": active,
            "host": self.host,
            "port": self.port,
            "uptime": uptime,
            "clients": clients,
        }

    # Returns connected client details for the CLI panel and dashboard.
    def Clients(self) -> list[dict]:
        if not self.IsActive():
            return []

        entries = self.server.registry.List()
        return [
            {
                "address": entry.address,
                "role": entry.role,
                "role_label": entry.RoleLabel(entry.role),
                "registered": entry.registered,
                "room_id": entry.room_id or "",
            }
            for entry in entries
        ]

    # Returns active game rooms for the CLI panel and dashboard.
    def Rooms(self) -> list[dict]:
        if not self.IsActive():
            return []

        return [
            {
                "id": room.id,
                "dm": room.dm_address,
                "visibility": room.visibility,
                "capacity": room.capacity,
                "players": room.PlayerCount(),
                "members": room.MemberCount(),
                "has_password": bool(room.password),
            }
            for room in self.server.rooms.List()
        ]

    # Stops the server when the CLI panel exits.
    def Cleanup(self) -> None:
        if self.IsActive():
            self.server.Stop()
            self.server = None
