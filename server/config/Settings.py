# Default network settings for local development and testing.
# Values can be changed from the Settings panel or loaded from stored.json.


class Settings:
    # Custom host used when Mode is set to "Custom".
    Host = "127.0.0.1"

    # TCP port the central server listens on.
    Port = 5555

    # Listen mode: "Local" (127.0.0.1), "Network" (0.0.0.0), or "Custom" (uses Host).
    Mode = "Local"

    # Maximum simultaneous clients (0 = unlimited).
    MaxClients = 0

    # Whether the server starts automatically when the panel opens.
    AutoStart = True


def ResolveHost() -> str:
    # Returns the bind address based on the current listen mode.
    if Settings.Mode == "Local":
        return "127.0.0.1"

    if Settings.Mode == "Network":
        return "0.0.0.0"

    return Settings.Host
