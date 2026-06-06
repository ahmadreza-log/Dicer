import json


class Protocol:
    # Newline-delimited JSON messages for client registration.

    ValidRoles = {"dm", "adventure", "watch"}
    ValidVisibility = {"public", "private"}

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
    def Registered(
        cls,
        ok: bool,
        role: str = "",
        error: str = "",
        room: dict | None = None,
    ) -> dict:
        message = {"type": "registered", "ok": ok}

        if ok:
            message["role"] = role

            if room:
                message["room"] = room
        elif error:
            message["error"] = error

        return message

    @classmethod
    def ParseRoomSettings(cls, payload: dict | None) -> tuple[str | None, str | None, int | None]:
        if not isinstance(payload, dict):
            return None, None, None

        visibility = str(payload.get("visibility", "")).strip().lower()
        password = str(payload.get("password", ""))
        capacity = payload.get("capacity")

        resolved_visibility = visibility if visibility in cls.ValidVisibility else None
        resolved_capacity = (
            int(capacity) if isinstance(capacity, (int, float)) and int(capacity) > 0 else None
        )

        return resolved_visibility, password, resolved_capacity
