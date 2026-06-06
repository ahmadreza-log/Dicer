import socket
import time


class Room:
    # A single game session owned by a connected Dungeon Master.

    def __init__(
        self,
        id: str,
        host_peer: socket.socket,
        dm_address: str,
        visibility: str,
        password: str,
        capacity: int,
    ) -> None:
        self.id = id
        self.host_peer = host_peer
        self.dm_address = dm_address
        self.visibility = visibility
        self.password = password
        self.capacity = capacity
        self.created_at = time.time()

    def ToDict(self) -> dict:
        payload = {
            "id": self.id,
            "visibility": self.visibility,
            "capacity": self.capacity,
        }

        if self.password:
            payload["password"] = self.password

        return payload
