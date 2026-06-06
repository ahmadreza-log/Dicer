# Connection-related settings for client handlers.


class Settings:
    # Message sent to each client immediately after connecting.
    Welcome = "Connected to Dicer server"

    # Socket receive buffer size in bytes.
    Buffer = 4096

    # Idle timeout in seconds before disconnecting (0 = no timeout).
    Timeout = 0

    # Maximum connections from a single IP address (0 = unlimited).
    MaxPerAddress = 0
