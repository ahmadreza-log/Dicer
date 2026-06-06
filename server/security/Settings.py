# Security settings for client access control.
# Password verification will be enforced once the client protocol is implemented.


class Settings:
    # Optional password clients must provide (empty = no password required).
    Password = ""

    # Comma-separated list of allowed IP addresses (empty = allow all).
    Allowed = ""

    # Comma-separated list of blocked IP addresses.
    Blocked = ""

    @staticmethod
    def ParseList(raw: str) -> list[str]:
        if not raw.strip():
            return []

        return [item.strip() for item in raw.split(",") if item.strip()]
