import json


class Protocol:
    ValidRoles = {"dm", "adventure", "watch"}

    Labels = {
        "dm": "Dungeon Master",
        "adventure": "Adventurer",
        "watch": "Spectator",
    }

    @classmethod
    def Register(cls, role: str) -> bytes:
        payload = {"type": "register", "role": role}
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
