import socket


class Entry:
    # Represents a single active client connection tracked by the registry.

    def __init__(self, peer: socket.socket, address: tuple[str, int]) -> None:
        self.peer = peer
        self.host = address[0]
        self.port = address[1]
