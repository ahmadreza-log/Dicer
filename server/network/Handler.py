import socket
from collections.abc import Callable

from connection.Settings import Settings as Connection
from logger.Logger import Logger
from network.Protocol import Protocol
from network.Registry import Registry
from room.Registry import Registry as RoomRegistry


class Handler:
    # Handles the full lifecycle of a single client connection:
    # welcome message, receive loop, cleanup on disconnect.

    def __init__(
        self,
        peer: socket.socket,
        address: tuple[str, int],
        registry: Registry,
        rooms: RoomRegistry,
        running: Callable[[], bool],
    ) -> None:
        self.peer = peer
        self.address = address
        self.registry = registry
        self.rooms = rooms
        self.running = running
        self.logger = Logger.Get("Handler")
        self.buffer = ""

    # Runs on a dedicated thread for each connected client.
    def Run(self) -> None:
        self.logger.debug(
            "Handler started | address=%s | port=%d",
            self.address[0],
            self.address[1],
        )

        self.registry.Add(self.peer, self.address)

        try:
            if Connection.Timeout > 0:
                self.peer.settimeout(float(Connection.Timeout))

            welcome = f"{Connection.Welcome}\n".encode("utf-8")
            self.peer.sendall(welcome)
            self.logger.debug(
                "Welcome message sent | address=%s | port=%d",
                self.address[0],
                self.address[1],
            )
            self.ReceiveLoop()
        except (ConnectionResetError, TimeoutError, OSError) as error:
            self.logger.warning(
                "Connection error | address=%s | port=%d | reason=%s",
                self.address[0],
                self.address[1],
                error,
            )
        finally:
            self.Disconnect()

    # Continuously reads incoming data until the client closes or the server stops.
    def ReceiveLoop(self) -> None:
        while self.running():
            try:
                payload = self.peer.recv(Connection.Buffer)
            except TimeoutError:
                self.logger.info(
                    "Client idle timeout | address=%s | port=%d",
                    self.address[0],
                    self.address[1],
                )
                break

            if not payload:
                self.logger.info(
                    "Client closed connection | address=%s | port=%d",
                    self.address[0],
                    self.address[1],
                )
                break

            text = payload.decode("utf-8", errors="replace")
            self.buffer += text
            self.ProcessBuffer()

    # Parses complete newline-delimited messages from the receive buffer.
    def ProcessBuffer(self) -> None:
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.split("\n", 1)
            line = line.strip()

            if line:
                self.HandleLine(line)

    # Handles a single decoded client message.
    def HandleLine(self, line: str) -> None:
        self.logger.info(
            "Message received | address=%s | port=%d | text=%s",
            self.address[0],
            self.address[1],
            line,
        )

        message = Protocol.Parse(line)

        if message is None:
            self.Reply(Protocol.Registered(False, error="Invalid message format."))
            return

        if message.get("type") == "register":
            self.HandleRegister(message)
            return

        self.Reply(Protocol.Registered(False, error="Unknown message type."))

    # Registers the client role sent after connect.
    def HandleRegister(self, message: dict) -> None:
        role = str(message.get("role", "")).strip().lower()

        if role not in Protocol.ValidRoles:
            self.Reply(Protocol.Registered(False, error="Invalid role."))
            return

        success, reason = self.registry.Register(self.peer, role)

        if not success:
            self.Reply(Protocol.Registered(False, error=reason))
            return

        room_payload = None

        if role == "dm":
            visibility, password, capacity = Protocol.ParseRoomSettings(message.get("room"))
            dm_address = f"{self.address[0]}:{self.address[1]}"
            room = self.rooms.Create(
                host_peer=self.peer,
                dm_address=dm_address,
                visibility=visibility,
                password=password,
                capacity=capacity,
            )
            entry = self.registry.Find(self.peer)

            if entry is not None:
                entry.room_id = room.id

            room_payload = room.ToDict()
            self._LogActivity(
                f"Room {room.id} created by Dungeon Master from {dm_address}",
            )

        self.Reply(Protocol.Registered(True, role=role, room=room_payload))

    # Writes to the dashboard activity feed when the panel is active.
    def _LogActivity(self, message: str) -> None:
        try:
            from board.Bridge import Bridge

            Bridge.Log(message, "success")
        except ImportError:
            self.logger.info(message)

    # Sends a JSON response line to the client.
    def Reply(self, payload: dict) -> None:
        try:
            self.peer.sendall(Protocol.Encode(payload) + b"\n")
        except OSError as error:
            self.logger.warning(
                "Reply failed | address=%s | port=%d | reason=%s",
                self.address[0],
                self.address[1],
                error,
            )

    # Removes the client from the registry and closes its socket.
    def Disconnect(self) -> None:
        entry = self.registry.Find(self.peer)

        if entry is not None and entry.room_id:
            self.rooms.Remove(entry.room_id)

        self.registry.Remove(self.peer)
        self.peer.close()
        self.logger.info(
            "Client disconnected | address=%s | port=%d",
            self.address[0],
            self.address[1],
        )
