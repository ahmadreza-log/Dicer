import socket

from Settings import Settings


class Probe:
    # Lightweight TCP reachability check for the network settings screen.

    @classmethod
    def Test(cls, host: str, port: int) -> tuple[bool, str]:
        try:
            peer = socket.create_connection((host, port), timeout=Settings.Timeout)
        except OSError as error:
            return False, f"Could not connect to {host}:{port}. {error}"

        try:
            chunk = peer.recv(4096)

            if not chunk:
                peer.close()
                return False, "Server closed the connection."

            welcome = chunk.decode("utf-8", errors="replace").strip()
            peer.close()
            return True, welcome or "Connected successfully."
        except OSError as error:
            peer.close()
            return False, str(error)
