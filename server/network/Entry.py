import socket
import time


class Entry:
    # Represents a single active client connection tracked by the registry.

    Labels = {
        "dm": "Dungeon Master",
        "adventure": "Adventurer",
        "watch": "Spectator",
    }

    def __init__(self, peer: socket.socket, address: tuple[str, int]) -> None:
        self.peer = peer
        self.host = address[0]
        self.port = address[1]
        self.role: str | None = None
        self.registered = False
        self.connected_at = time.time()

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"

    @classmethod
    def RoleLabel(cls, role: str | None) -> str:
        if not role:
            return "Pending"

        return cls.Labels.get(role, role)
