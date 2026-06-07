import socket
import threading

from logger.Logger import Logger
from room.Id import Id
from room.Room import Room
from room.Settings import Settings as Defaults


class Registry:
    # Thread-safe store of active game rooms keyed by short id.

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.rooms: dict[str, Room] = {}
        self.logger = Logger.Get("RoomRegistry")

    # Creates a room for a Dungeon Master and returns it.
    def Create(
        self,
        host_peer: socket.socket,
        dm_address: str,
        visibility: str | None = None,
        password: str | None = None,
        capacity: int | None = None,
        campaign_name: str = "",
        campaign_id: int | None = None,
    ) -> Room:
        resolved_visibility = visibility or Defaults.Visibility
        resolved_password = password if password is not None else Defaults.Password
        resolved_capacity = capacity if capacity is not None else Defaults.Capacity

        with self.lock:
            room_id = self._UniqueId()
            room = Room(
                id=room_id,
                host_peer=host_peer,
                dm_address=dm_address,
                visibility=resolved_visibility,
                password=resolved_password,
                capacity=resolved_capacity,
                campaign_name=campaign_name,
                campaign_id=campaign_id,
            )
            self.rooms[room_id] = room

        self.logger.info(
            "Room created | id=%s | dm=%s | visibility=%s | capacity=%d",
            room_id,
            dm_address,
            resolved_visibility,
            resolved_capacity,
        )
        return room

    # Adds a client to an existing room after validation.
    def Join(
        self,
        room_id: str,
        peer: socket.socket,
        role: str,
        password: str = "",
    ) -> tuple[bool, str, Room | None]:
        with self.lock:
            room = self.rooms.get(room_id)

            if room is None:
                return False, "Room not found.", None

            if peer is room.host_peer:
                return False, "Dungeon Master cannot join as a member.", None

            if peer in room.members:
                return False, "Already in this room.", None

            if room.password and room.password != password:
                return False, "Incorrect room password.", None

            if role == "adventure" and room.PlayerCount() >= room.capacity:
                return False, "Room is full.", None

            room.members[peer] = role

        self.logger.info(
            "Client joined room | id=%s | role=%s | players=%d | members=%d",
            room_id,
            role,
            room.PlayerCount(),
            room.MemberCount(),
        )
        return True, "", room

    # Removes a member from their room without deleting the session.
    def Leave(self, peer: socket.socket) -> None:
        with self.lock:
            for room in self.rooms.values():
                if peer in room.members:
                    role = room.members.pop(peer)
                    room_id = room.id
                    break
            else:
                return

        self.logger.info("Client left room | id=%s | role=%s", room_id, role)

    # Returns a room by id, or None when it does not exist.
    def Get(self, room_id: str) -> Room | None:
        with self.lock:
            return self.rooms.get(room_id)

    # Removes a room when its Dungeon Master disconnects.
    def Remove(self, room_id: str) -> None:
        with self.lock:
            removed = self.rooms.pop(room_id, None)

        if removed:
            self.logger.info("Room removed | id=%s | dm=%s", room_id, removed.dm_address)

    # Returns the room owned by a specific client socket.
    def FindByPeer(self, peer: socket.socket) -> Room | None:
        with self.lock:
            for room in self.rooms.values():
                if room.host_peer is peer:
                    return room

                if peer in room.members:
                    return room

        return None

    # Returns the active room tied to a saved campaign id, if any.
    def FindByCampaignId(self, campaign_id: int) -> Room | None:
        with self.lock:
            for room in self.rooms.values():
                if room.campaign_id == campaign_id:
                    return room

        return None

    # Returns a snapshot of all active rooms.
    def List(self) -> list[Room]:
        with self.lock:
            return list(self.rooms.values())

    def _UniqueId(self) -> str:
        while True:
            candidate = Id.Generate()

            if candidate not in self.rooms:
                return candidate
