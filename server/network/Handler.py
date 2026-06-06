import socket
from collections.abc import Callable

from connection.Settings import Settings as Connection
from logger.Logger import Logger
from network.Registry import Registry


class Handler:
    # Handles the full lifecycle of a single client connection:
    # welcome message, receive loop, cleanup on disconnect.

    def __init__(
        self,
        peer: socket.socket,
        address: tuple[str, int],
        registry: Registry,
        running: Callable[[], bool],
    ) -> None:
        self.peer = peer
        self.address = address
        self.registry = registry
        self.running = running
        self.logger = Logger.Get("Handler")

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

            text = payload.decode("utf-8", errors="replace").strip()
            self.logger.info(
                "Message received | address=%s | port=%d | bytes=%d | text=%s",
                self.address[0],
                self.address[1],
                len(payload),
                text,
            )

    # Removes the client from the registry and closes its socket.
    def Disconnect(self) -> None:
        self.registry.Remove(self.peer)
        self.peer.close()
        self.logger.info(
            "Client disconnected | address=%s | port=%d",
            self.address[0],
            self.address[1],
        )
