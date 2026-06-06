import json
from pathlib import Path

from Settings import Settings


class Store:
    # Persists client settings to a JSON file beside the client entry point.

    Filename = "stored.json"

    @classmethod
    def Path(cls) -> Path:
        return Path(__file__).resolve().parent / cls.Filename

    @classmethod
    def Load(cls) -> None:
        filepath = cls.Path()

        if not filepath.is_file():
            return

        try:
            data = json.loads(filepath.read_text(encoding="utf-8"))
            network = data.get("network", {})
            Settings.ApplyHost(str(network.get("Host", Settings.Host)))
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            pass

    @classmethod
    def Save(cls) -> tuple[bool, str]:
        filepath = cls.Path()
        payload = {
            "network": {
                "Host": Settings.Host,
            },
        }

        try:
            filepath.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            return True, "Settings saved."
        except OSError as error:
            return False, str(error)
