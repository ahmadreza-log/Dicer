import json


class Protocol:
    ValidRoles = {"dm", "adventure", "watch"}

    Labels = {
        "guest": "Guest",
        "dm": "Dungeon Master",
        "adventure": "Player",
        "watch": "Spectator",
    }

    DefaultRole = "guest"

    @classmethod
    def Register(cls, role: str, room: dict | None = None) -> bytes:
        payload: dict = {"type": "register", "role": role}

        if room:
            payload["room"] = room

        return json.dumps(payload, separators=(",", ":")).encode("utf-8") + b"\n"

    @classmethod
    def Parse(cls, line: str) -> dict | None:
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            return None

        return payload if isinstance(payload, dict) else None

    @classmethod
    def Label(cls, role: str) -> str:
        return cls.Labels.get(role, role)
