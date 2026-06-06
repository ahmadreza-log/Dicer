import socket
import threading

from config.Settings import Settings as Network
from connection.Settings import Settings as Connection
from logger.Logger import Logger
from network.Entry import Entry


class Registry:
    # Keeps track of every active client connection in a thread-safe list.

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.entries: list[Entry] = []
        self.logger = Logger.Get("Registry")

    # Adds a newly accepted client socket to the registry.
    def Add(self, peer: socket.socket, address: tuple[str, int]) -> None:
        with self.lock:
            self.entries.append(Entry(peer=peer, address=address))
            total = len(self.entries)

        self.logger.debug("Peer registered | active=%d", total)

    # Removes a disconnected client socket from the registry.
    def Remove(self, peer: socket.socket) -> None:
        with self.lock:
            self.entries = [entry for entry in self.entries if entry.peer is not peer]
            total = len(self.entries)

        self.logger.debug("Peer removed | active=%d", total)

    # Returns the number of currently connected clients.
    def Count(self) -> int:
        with self.lock:
            return len(self.entries)

    # Returns how many clients are connected from a specific host address.
    def CountHost(self, host: str) -> int:
        with self.lock:
            return sum(1 for entry in self.entries if entry.host == host)

    # Checks whether a new connection is allowed under current limits.
    def CanAccept(self, host: str) -> tuple[bool, str]:
        total = self.Count()

        if Network.MaxClients > 0 and total >= Network.MaxClients:
            return False, "Maximum client limit reached."

        per = self.CountHost(host)

        if Connection.MaxPerAddress > 0 and per >= Connection.MaxPerAddress:
            return False, f"Maximum connections from {host} reached."

        return True, ""

    # Returns a snapshot copy of all active client entries.
    def List(self) -> list[Entry]:
        with self.lock:
            return list(self.entries)

    # Closes every registered client and clears the list during shutdown.
    def CloseAll(self) -> None:
        with self.lock:
            total = len(self.entries)

            for entry in self.entries:
                entry.peer.close()

            self.entries.clear()

        self.logger.info("All peers closed | count=%d", total)
