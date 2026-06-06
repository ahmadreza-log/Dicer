import socket
import threading

from Settings import Settings
from network.Protocol import Protocol


class Session:
    # Keeps a live TCP connection after the client registers with the server.

    peer: socket.socket | None = None
    role: str | None = None
    thread: threading.Thread | None = None
    running = False

    @classmethod
    def IsConnected(cls) -> bool:
        return cls.peer is not None

    @classmethod
    def Register(cls, role: str) -> tuple[bool, str]:
        if role not in Protocol.ValidRoles:
            return False, "Invalid role."

        cls.Disconnect()

        try:
            peer = socket.create_connection(
                (Settings.Host, Settings.Port),
                timeout=Settings.Timeout,
            )
        except OSError as error:
            return False, f"Could not connect to {Settings.Host}:{Settings.Port}. {error}"

        try:
            welcome = cls.ReadLine(peer)

            if not welcome:
                peer.close()
                return False, "Server closed the connection."

            peer.sendall(Protocol.Register(role))
            response = cls.ReadLine(peer)

            if not response:
                peer.close()
                return False, "No response from server."

            payload = Protocol.Parse(response)

            if payload is None or not payload.get("ok"):
                peer.close()
                error = payload.get("error", "Registration failed.") if payload else "Registration failed."
                return False, error

            cls.peer = peer
            cls.role = role
            cls.running = True
            cls.thread = threading.Thread(target=cls.Listen, daemon=True)
            cls.thread.start()
            return True, Protocol.Label(role)

        except OSError as error:
            peer.close()
            return False, str(error)

    @classmethod
    def ReadLine(cls, peer: socket.socket) -> str:
        buffer = ""

        while "\n" not in buffer:
            chunk = peer.recv(4096)

            if not chunk:
                return ""

            buffer += chunk.decode("utf-8", errors="replace")

        line, _rest = buffer.split("\n", 1)
        return line.strip()

    @classmethod
    def Listen(cls) -> None:
        while cls.running and cls.peer is not None:
            try:
                chunk = cls.peer.recv(4096)
            except OSError:
                break

            if not chunk:
                break

        cls.Disconnect()

    @classmethod
    def Disconnect(cls) -> None:
        cls.running = False

        if cls.peer is not None:
            try:
                cls.peer.close()
            except OSError:
                pass

        cls.peer = None
        cls.role = None
