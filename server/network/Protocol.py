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
    def Error(cls, error: str, response_type: str = "error") -> dict:
        return {"type": response_type, "ok": False, "error": error}

    @classmethod
    def Campaigns(cls, ok: bool, items: list[dict] | None = None, error: str = "") -> dict:
        message = {"type": "campaigns", "ok": ok}

        if ok:
            message["items"] = items or []
        elif error:
            message["error"] = error

        return message

    @classmethod
    def CampaignSaved(cls, ok: bool, campaign: dict | None = None, error: str = "") -> dict:
        message = {"type": "campaign_saved", "ok": ok}

        if ok and campaign:
            message["campaign"] = campaign
        elif error:
            message["error"] = error

        return message

    @classmethod
    def ParseOwner(cls, message: dict) -> str:
        return str(message.get("owner_id", "")).strip()

    @classmethod
    def ParseCampaignForm(cls, message: dict) -> tuple[str, int, bool, str]:
        name = str(message.get("name", "")).strip()
        capacity = message.get("capacity", 0)
        is_private = bool(message.get("private"))
        password = str(message.get("password", ""))
        resolved_capacity = int(capacity) if isinstance(capacity, (int, float)) else 0
        return name, resolved_capacity, is_private, password

    @classmethod
    def ParseRoomSettings(
        cls,
        payload: dict | None,
    ) -> tuple[str | None, str | None, int | None, str]:
        if not isinstance(payload, dict):
            return None, None, None, ""

        visibility = str(payload.get("visibility", "")).strip().lower()
        password = str(payload.get("password", ""))
        capacity = payload.get("capacity")
        name = str(payload.get("name", "")).strip()

        if payload.get("private") is True:
            visibility = "private"
        elif payload.get("private") is False and not visibility:
            visibility = "public"

        resolved_visibility = visibility if visibility in cls.ValidVisibility else None
        resolved_capacity = (
            int(capacity) if isinstance(capacity, (int, float)) and int(capacity) > 0 else None
        )

        return resolved_visibility, password, resolved_capacity, name

    @classmethod
    def ParseJoin(cls, message: dict) -> tuple[str, str]:
        room_id = str(message.get("room_id", "")).strip()
        password = str(message.get("password", ""))
        return room_id, password
