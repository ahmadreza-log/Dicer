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
    def ListCampaigns(cls) -> bytes:
        payload = {
            "type": "list_campaigns",
            "owner_id": Store.OwnerId,
        }
        return cls.Encode(payload)

    @classmethod
    def SaveCampaign(cls, name: str, capacity: int, private: bool, password: str) -> bytes:
        payload = {
            "type": "save_campaign",
            "owner_id": Store.OwnerId,
            "name": name,
            "capacity": capacity,
            "private": private,
            "password": password,
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
            "owner_id": Store.OwnerId,
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
