from security.Settings import Settings


class Guard:
    # Validates incoming client addresses against security rules.

    @staticmethod
    def Allow(host: str) -> tuple[bool, str]:
        blocked = Settings.ParseList(Settings.Blocked)

        if host in blocked:
            return False, f"Blocked address: {host}"

        allowed = Settings.ParseList(Settings.Allowed)

        if allowed and host not in allowed:
            return False, f"Address not in allowed list: {host}"

        return True, ""
