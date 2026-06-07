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
        campaign_name: str = "",
        campaign_id: int | None = None,
    ) -> None:
        self.id = id
        self.host_peer = host_peer
        self.dm_address = dm_address
        self.visibility = visibility
        self.password = password
        self.capacity = capacity
        self.campaign_name = campaign_name
        self.campaign_id = campaign_id
        self.created_at = time.time()
        self.members: dict[socket.socket, str] = {}

    def PlayerCount(self) -> int:
        return sum(1 for role in self.members.values() if role == "adventure")

    def MemberCount(self) -> int:
        return len(self.members)

    def ToDict(self, include_password: bool = False) -> dict:
        payload = {
            "id": self.id,
            "visibility": self.visibility,
            "capacity": self.capacity,
            "players": self.PlayerCount(),
            "members": self.MemberCount(),
        }

        if self.campaign_name:
            payload["name"] = self.campaign_name

        if self.campaign_id is not None:
            payload["campaign_id"] = self.campaign_id

        if include_password and self.password:
            payload["password"] = self.password

        return payload
