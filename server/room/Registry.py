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
