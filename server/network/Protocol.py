import json


class Protocol:
    # Newline-delimited JSON messages for client registration.

    ValidRoles = {"dm", "adventure", "watch"}

    @classmethod
    def Parse(cls, line: str) -> dict | None:
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            return None

        return payload if isinstance(payload, dict) else None

    @classmethod
    def Encode(cls, payload: dict) -> bytes:
        return json.dumps(payload, separators=(",", ":")).encode("utf-8")

    @classmethod
    def Registered(cls, ok: bool, role: str = "", error: str = "") -> dict:
        message = {"type": "registered", "ok": ok}

        if ok:
            message["role"] = role
        elif error:
            message["error"] = error

        return message
