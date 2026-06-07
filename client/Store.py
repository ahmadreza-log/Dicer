import json
from pathlib import Path

from Settings import Settings


class Store:
    # Persists client settings to a JSON file beside the client entry point.

    Filename = "stored.json"
    LocaleCode = "en"
    UserId = 0
    Username = ""
    Email = ""
    Active = False

    @classmethod
    def Path(cls) -> Path:
        return Path(__file__).resolve().parent / cls.Filename

    @classmethod
    def Read(cls) -> dict:
        filepath = cls.Path()

        if not filepath.is_file():
            return {}

        try:
            data = json.loads(filepath.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            return {}

    @classmethod
    def Load(cls) -> None:
        data = cls.Read()
        network = data.get("network", {})
        Settings.ApplyHost(str(network.get("Host", Settings.Host)))

        cls.LocaleCode = str(data.get("locale", cls.LocaleCode)).strip() or cls.LocaleCode

        user = data.get("user", {})
        cls.UserId = int(user.get("id", 0) or 0)
        cls.Username = str(user.get("username", "")).strip()
        cls.Email = str(user.get("email", "")).strip()
        cls.Active = bool(user.get("active", user.get("email_verified", False)))

    @classmethod
    def Snapshot(cls) -> dict:
        return {
            "locale": cls.LocaleCode,
            "user": {
                "id": cls.UserId,
                "username": cls.Username,
                "email": cls.Email,
                "active": cls.Active,
            },
            "network": {
                "Host": Settings.Host,
            },
        }

    @classmethod
    def Write(cls, payload: dict) -> tuple[bool, str]:
        try:
            cls.Path().write_text(json.dumps(payload, indent=2), encoding="utf-8")
            return True, "store.saved"
        except OSError as error:
            return False, str(error)

    @classmethod
    def Save(cls) -> tuple[bool, str]:
        saved, message = cls.Write(cls.Snapshot())
        return saved, message

    @classmethod
    def SaveLocale(cls, code: str) -> tuple[bool, str]:
        cls.LocaleCode = code
        return cls.Save()

    @classmethod
    def SaveUser(cls, user: dict) -> tuple[bool, str]:
        cls.UserId = int(user.get("id", 0) or 0)
        cls.Username = str(user.get("username", "")).strip()
        cls.Email = str(user.get("email", "")).strip()
        cls.Active = bool(user.get("active", user.get("email_verified", False)))
        return cls.Save()

    @classmethod
    def ClearUser(cls) -> tuple[bool, str]:
        cls.UserId = 0
        cls.Username = ""
        cls.Email = ""
        cls.Active = False
        return cls.Save()
