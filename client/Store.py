import json
import uuid
from pathlib import Path

from Settings import Settings


class Store:
    # Persists client settings to a JSON file beside the client entry point.

    Filename = "stored.json"
    OwnerId = ""
    LocaleCode = "en"

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

        owner_id = str(data.get("owner_id", "")).strip()

        if owner_id:
            cls.OwnerId = owner_id
        else:
            cls.OwnerId = uuid.uuid4().hex

        cls.LocaleCode = str(data.get("locale", cls.LocaleCode)).strip() or cls.LocaleCode

    @classmethod
    def Snapshot(cls) -> dict:
        if not cls.OwnerId:
            cls.OwnerId = uuid.uuid4().hex

        return {
            "owner_id": cls.OwnerId,
            "locale": cls.LocaleCode,
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
