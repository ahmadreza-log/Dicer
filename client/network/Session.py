import socket
import threading

from Settings import Settings
from network.Protocol import Protocol


class Session:
    # Persistent TCP connection to the central server.

    peer: socket.socket | None = None
    role: str | None = None
    room: dict | None = None
    thread: threading.Thread | None = None
    running = False
    _buffer = ""
    _lock = threading.Lock()
    _room_closed_handler = None

    @classmethod
    def SetRoomClosedHandler(cls, handler) -> None:
        cls._room_closed_handler = handler

    @classmethod
    def InRoom(cls) -> bool:
        return cls.role in Protocol.ValidRoles and cls.room is not None

    @classmethod
    def IsConnected(cls) -> bool:
        return cls.peer is not None

    @classmethod
    def Connect(cls) -> tuple[bool, str]:
        if cls.IsConnected():
            return True, "Already connected to server."

        cls.Disconnect()
        cls._buffer = ""

        try:
            peer = socket.create_connection(
                (Settings.Host, Settings.Port),
                timeout=Settings.Timeout,
            )
        except OSError as error:
            return False, f"Could not connect to {Settings.Host}:{Settings.Port}. {error}"

        try:
            peer.settimeout(Settings.Timeout)
            welcome = cls.ReadLine(peer)

            if not welcome:
                peer.close()
                return False, "Server closed the connection."

            peer.settimeout(None)
            cls.peer = peer
            cls.role = Protocol.DefaultRole
            return True, welcome

        except OSError as error:
            peer.close()
            return False, str(error)

    @classmethod
    def Request(cls, payload: bytes) -> tuple[bool, dict | str]:
        cls._StopListen()

        if not cls.IsConnected():
            success, message = cls.Connect()

            if not success:
                return False, message

        with cls._lock:
            try:
                cls.peer.sendall(payload)
                response = cls.ReadLine(cls.peer)

                if not response:
                    return False, "No response from server."

                parsed = Protocol.Parse(response)

                if parsed is None:
                    return False, "Invalid response from server."

                if not parsed.get("ok"):
                    return False, parsed.get("error", "Request failed.")

                return True, parsed

            except OSError as error:
                return False, str(error)

    @classmethod
    def ListCampaigns(cls) -> tuple[bool, list[dict] | str]:
        success, payload = cls.Request(Protocol.ListCampaigns())

        if not success:
            return False, payload if isinstance(payload, str) else "Request failed."

        items = payload.get("items", [])
        return True, items if isinstance(items, list) else []

    @classmethod
    def SaveCampaign(
        cls,
        name: str,
        capacity: int,
        private: bool,
        password: str,
    ) -> tuple[bool, dict | str]:
        success, payload = cls.Request(Protocol.SaveCampaign(name, capacity, private, password))

        if not success:
            return False, payload if isinstance(payload, str) else "Request failed."

        campaign = payload.get("campaign")

        if not isinstance(campaign, dict):
            return False, "Campaign was not saved."

        return True, campaign

    @classmethod
    def LoginUser(cls, login: str, password: str) -> tuple[bool, dict | str]:
        success, payload = cls.Request(Protocol.LoginUser(login, password))

        if not success:
            return False, payload if isinstance(payload, str) else "Request failed."

        user = payload.get("user")

        if not isinstance(user, dict):
            return False, "Sign in failed."

        return True, user

    @classmethod
    def RegisterUser(cls, username: str, email: str, password: str) -> tuple[bool, dict | str]:
        success, payload = cls.Request(Protocol.RegisterUser(username, email, password))

        if not success:
            return False, payload if isinstance(payload, str) else "Request failed."

        user = payload.get("user")

        if not isinstance(user, dict):
            return False, "Registration failed."

        return True, user

    @classmethod
    def VerifyEmail(cls, user_id: int, code: str) -> tuple[bool, dict | str]:
        success, payload = cls.Request(Protocol.VerifyEmail(user_id, code))

        if not success:
            return False, payload if isinstance(payload, str) else "Request failed."

        user = payload.get("user")

        if not isinstance(user, dict):
            return False, "Verification failed."

        return True, user

    @classmethod
    def ResendActivation(cls, user_id: int) -> tuple[bool, str]:
        success, payload = cls.Request(Protocol.ResendActivation(user_id))

        if not success:
            return False, payload if isinstance(payload, str) else "Request failed."

        return True, "Verification code sent."

    @classmethod
    def EnsurePresence(cls) -> tuple[bool, str]:
        if cls.role in Protocol.ValidRoles:
            if not cls.running:
                cls.StartListen()
            return True, ""

        if cls.IsConnected():
            return True, ""

        return cls.Connect()

    @classmethod
    def Register(
        cls,
        role: str,
        room: dict | None = None,
        room_id: str = "",
        password: str = "",
        campaign_id: int | None = None,
    ) -> tuple[bool, str]:
        if role not in Protocol.ValidRoles:
            return False, "Invalid role."

        if role != "dm" and not room_id.strip():
            return False, "Room ID is required."

        if not cls.IsConnected():
            success, message = cls.Connect()

            if not success:
                return False, message

        cls._StopListen()

        with cls._lock:
            try:
                cls.peer.sendall(
                    Protocol.Register(role, room, room_id, password, campaign_id),
                )
                response = cls.ReadLine(cls.peer)

                if not response:
                    cls.Disconnect()
                    return False, "No response from server."

                payload = Protocol.Parse(response)

                if payload is None or not payload.get("ok"):
                    error = payload.get("error", "Registration failed.") if payload else "Registration failed."
                    return False, error

                cls.role = role
                cls.room = payload.get("room") if isinstance(payload.get("room"), dict) else None
                cls.StartListen()
                return True, Protocol.Label(role)

            except OSError as error:
                cls.Disconnect()
                return False, str(error)

    @classmethod
    def LeaveRoom(cls) -> tuple[bool, str]:
        if not cls.InRoom():
            return False, "Not in a room."

        cls._StopListen()

        with cls._lock:
            try:
                cls.peer.sendall(Protocol.LeaveRoom())
                response = cls.ReadLine(cls.peer)

                if not response:
                    return False, "No response from server."

                payload = Protocol.Parse(response)

                if payload is None or not payload.get("ok"):
                    error = payload.get("error", "Could not leave the room.") if payload else "Could not leave the room."
                    return False, error

                cls.role = Protocol.DefaultRole
                cls.room = None
                return True, ""

            except OSError as error:
                cls.Disconnect()
                return False, str(error)

    @classmethod
    def StartListen(cls) -> None:
        if cls.running or cls.peer is None:
            return

        cls.running = True
        cls.thread = threading.Thread(target=cls.Listen, name="SessionListen", daemon=True)
        cls.thread.start()

    @classmethod
    def _StopListen(cls) -> None:
        if not cls.running:
            return

        cls.running = False
        thread = cls.thread

        if thread is not None and thread.is_alive() and thread is not threading.current_thread():
            thread.join(timeout=1.5)

        cls.thread = None

    @classmethod
    def ReadLine(cls, peer: socket.socket) -> str:
        while "\n" not in cls._buffer:
            chunk = peer.recv(4096)

            if not chunk:
                return ""

            cls._buffer += chunk.decode("utf-8", errors="replace")

        line, cls._buffer = cls._buffer.split("\n", 1)
        return line.strip()

    @classmethod
    def Listen(cls) -> None:
        while cls.running and cls.peer is not None:
            try:
                with cls._lock:
                    peer = cls.peer

                if peer is None:
                    break

                peer.settimeout(1.0)
                chunk = peer.recv(4096)
                peer.settimeout(None)
            except TimeoutError:
                continue
            except OSError:
                break

            if not chunk:
                break

            cls._buffer += chunk.decode("utf-8", errors="replace")

            while "\n" in cls._buffer:
                line, cls._buffer = cls._buffer.split("\n", 1)
                cls._HandlePush(line.strip())

        if cls.running:
            cls._HandleDisconnect()

    @classmethod
    def _HandlePush(cls, line: str) -> None:
        if not line:
            return

        payload = Protocol.Parse(line)

        if payload is None:
            return

        if payload.get("type") != "room_closed":
            return

        reason = str(payload.get("reason", "") or "")
        handler = cls._room_closed_handler
        cls.running = False

        if handler is not None:
            handler(reason)
            return

        cls.Disconnect()

    @classmethod
    def _HandleDisconnect(cls) -> None:
        was_in_room = cls.InRoom()
        handler = cls._room_closed_handler if was_in_room else None
        cls.Disconnect()

        if handler is not None:
            handler("")

    @classmethod
    def Disconnect(cls) -> None:
        cls._StopListen()

        if cls.peer is not None:
            try:
                cls.peer.close()
            except OSError:
                pass

        cls.peer = None
        cls.role = None
        cls.room = None
        cls._buffer = ""
