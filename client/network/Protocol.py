import json

from Store import Store


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
    def Encode(cls, payload: dict) -> bytes:
        return json.dumps(payload, separators=(",", ":")).encode("utf-8") + b"\n"

    @classmethod
    def _UserPayload(cls) -> dict:
        payload: dict = {}

        if Store.UserId:
            payload["user_id"] = Store.UserId

        return payload

    @classmethod
    def ListCampaigns(cls) -> bytes:
        payload = {
            "type": "list_campaigns",
            **_UserPayload(),
        }
        return cls.Encode(payload)

    @classmethod
    def SaveCampaign(cls, name: str, capacity: int, private: bool, password: str) -> bytes:
        payload = {
            "type": "save_campaign",
            "name": name,
            "capacity": capacity,
            "private": private,
            "password": password,
            **_UserPayload(),
        }
        return cls.Encode(payload)

    @classmethod
    def LoginUser(cls, login: str, password: str) -> bytes:
        payload = {
            "type": "login_user",
            "login": login,
            "password": password,
        }
        return cls.Encode(payload)

    @classmethod
    def RegisterUser(cls, username: str, email: str, password: str) -> bytes:
        payload = {
            "type": "register_user",
            "username": username,
            "email": email,
            "password": password,
        }
        return cls.Encode(payload)

    @classmethod
    def VerifyEmail(cls, user_id: int, code: str) -> bytes:
        payload = {
            "type": "verify_email",
            "user_id": user_id,
            "code": code,
        }
        return cls.Encode(payload)

    @classmethod
    def ResendActivation(cls, user_id: int) -> bytes:
        payload = {
            "type": "resend_activation",
            "user_id": user_id,
        }
        return cls.Encode(payload)

    @classmethod
    def Register(
        cls,
        role: str,
        room: dict | None = None,
        room_id: str = "",
        password: str = "",
        campaign_id: int | None = None,
    ) -> bytes:
        payload: dict = {
            "type": "register",
            "role": role,
            **_UserPayload(),
        }

        if role == "dm":
            if campaign_id is not None:
                payload["campaign_id"] = campaign_id
            elif room:
                payload["room"] = room
        elif room_id:
            payload["room_id"] = room_id.strip()

        if password:
            payload["password"] = password

        return cls.Encode(payload)

    @classmethod
    def Parse(cls, line: str) -> dict | None:
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            return None

        return payload if isinstance(payload, dict) else None

    @classmethod
    def Label(cls, role: str) -> str:
        from i18n.Locale import Locale

        return Locale.t(f"role.{role}")
