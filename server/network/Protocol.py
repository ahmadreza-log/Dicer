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
    def UserLoggedIn(cls, ok: bool, user: dict | None = None, error: str = "") -> dict:
        message = {"type": "user_logged_in", "ok": ok}

        if ok and user:
            message["user"] = user
        elif error:
            message["error"] = error

        return message

    @classmethod
    def UserRegistered(cls, ok: bool, user: dict | None = None, error: str = "") -> dict:
        message = {"type": "user_registered", "ok": ok}

        if ok and user:
            message["user"] = user
        elif error:
            message["error"] = error

        return message

    @classmethod
    def EmailVerified(cls, ok: bool, user: dict | None = None, error: str = "") -> dict:
        message = {"type": "email_verified", "ok": ok}

        if ok and user:
            message["user"] = user
        elif error:
            message["error"] = error

        return message

    @classmethod
    def ActivationSent(cls, ok: bool, error: str = "") -> dict:
        message = {"type": "activation_sent", "ok": ok}

        if error:
            message["error"] = error

        return message

    @classmethod
    def ParseLogin(cls, message: dict) -> tuple[str, str]:
        login = str(message.get("login", message.get("username", ""))).strip()
        password = str(message.get("password", ""))
        return login, password

    @classmethod
    def ParseCredentials(cls, message: dict) -> tuple[str, str, str]:
        username = str(message.get("username", "")).strip()
        email = str(message.get("email", "")).strip().lower()
        password = str(message.get("password", ""))
        return username, email, password

    @classmethod
    def ParseUserId(cls, message: dict) -> int | None:
        value = message.get("user_id")

        try:
            resolved = int(value)
        except (TypeError, ValueError):
            return None

        return resolved if resolved > 0 else None

    @classmethod
    def ParseVerificationCode(cls, message: dict) -> str:
        return str(message.get("code", "")).strip()

    @classmethod
    def PublicUser(cls, user: dict | None) -> dict | None:
        if user is None:
            return None

        return {
            "id": user["id"],
            "username": user.get("username", ""),
            "email": user.get("email", ""),
            "active": bool(user.get("active")),
        }

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
