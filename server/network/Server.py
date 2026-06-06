import socket
import threading
import time

from logger.Logger import Logger
from network.Handler import Handler
from network.Registry import Registry
from room.Registry import Registry as RoomRegistry
from security.Guard import Guard


class Server:
    # TCP central server that accepts client connections and delegates
    # each one to a Handler running on its own thread.

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.registry = Registry()
        self.rooms = RoomRegistry()
        self.running = False
        self.listener: socket.socket | None = None
        self.thread: threading.Thread | None = None
        self.started = 0.0
        self.reason = ""
        self.logger = Logger.Get("Server")

    # Starts the server in the current thread (blocks until stopped).
    def Start(self) -> None:
        self.Run()

    # Starts the server on a background thread (non-blocking).
    def Launch(self) -> None:
        if self.running:
            return

        self.thread = threading.Thread(target=self.Run, daemon=True)
        self.thread.start()

    # Sets up the listener and runs the accept loop.
    def Run(self) -> None:
        self.logger.debug("Creating TCP listener | host=%s | port=%d", self.host, self.port)
        self.reason = ""

        try:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.listener.bind((self.host, self.port))
            self.listener.listen()
            self.listener.settimeout(1.0)
            self.running = True
            self.started = time.time()

            self.logger.info("Server listening | host=%s | port=%d", self.host, self.port)
            self.AcceptLoop()
        except OSError as error:
            self.reason = str(error)
            self.logger.error("Server failed | reason=%s", error)
        finally:
            self.Stop()

    # Waits for incoming connections and spawns a Handler thread for each one.
    def AcceptLoop(self) -> None:
        while self.running:
            try:
                peer, address = self.listener.accept()
            except socket.timeout:
                continue
            except OSError as error:
                if self.running:
                    self.logger.error("Accept failed | reason=%s", error)
                break

            allowed, reason = Guard.Allow(address[0])

            if not allowed:
                self.logger.warning("Connection rejected | address=%s | reason=%s", address[0], reason)
                peer.close()
                continue

            accepted, reason = self.registry.CanAccept(address[0])

            if not accepted:
                self.logger.warning("Connection rejected | address=%s | reason=%s", address[0], reason)
                peer.close()
                continue

            self.logger.info(
                "Client connected | address=%s | port=%d",
                address[0],
                address[1],
            )

            handler = Handler(
                peer=peer,
                address=address,
                registry=self.registry,
                rooms=self.rooms,
                running=self.IsRunning,
            )

            thread = threading.Thread(target=handler.Run, daemon=True)
            thread.start()

    # Returns whether the server accept loop is still active.
    def IsRunning(self) -> bool:
        return self.running

    # Returns how many seconds the server has been running (0 if stopped).
    def Uptime(self) -> int:
        if not self.running:
            return 0

        return int(time.time() - self.started)

    # Returns the number of connected clients.
    def Clients(self) -> int:
        return self.registry.Count()

    # Stops the accept loop, closes all clients, and releases the listener socket.
    def Stop(self) -> None:
        if not self.running and self.listener is None:
            return

        self.logger.debug("Stopping server | host=%s | port=%d", self.host, self.port)
        self.running = False
        self.registry.CloseAll()

        if self.listener:
            self.listener.close()
            self.listener = None

        self.started = 0.0
        self.logger.info("Server stopped | host=%s | port=%d", self.host, self.port)
