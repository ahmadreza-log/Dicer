import json
from pathlib import Path

from config.Bundle import Bundle


class Store:
    # Persists settings to a JSON file inside the config folder.

    Filename = "stored.json"

    @classmethod
    def Path(cls) -> Path:
        return Path(__file__).resolve().parent / cls.Filename

    # Loads settings from disk if the file exists.
    @classmethod
    def Load(cls) -> tuple[bool, str]:
        filepath = cls.Path()

        if not filepath.exists():
            return False, "No saved settings file found."

        try:
            data = json.loads(filepath.read_text(encoding="utf-8"))
            Bundle.Apply(data)
            return True, f"Settings loaded from {cls.Filename}"
        except (json.JSONDecodeError, OSError, ValueError) as error:
            return False, f"Could not load settings. Reason: {error}"

    # Saves the current settings to disk.
    @classmethod
    def Save(cls) -> tuple[bool, str]:
        filepath = cls.Path()

        try:
            filepath.write_text(
                json.dumps(Bundle.Snapshot(), indent=2),
                encoding="utf-8",
            )
            return True, f"Settings saved to {cls.Filename}"
        except OSError as error:
            return False, f"Could not save settings. Reason: {error}"

    # Deletes the saved settings file and restores defaults.
    @classmethod
    def Reset(cls) -> tuple[bool, str]:
        Bundle.Reset()

        filepath = cls.Path()

        if filepath.exists():
            try:
                filepath.unlink()
            except OSError as error:
                return False, f"Defaults restored but file delete failed. Reason: {error}"

        return True, "Settings reset to defaults."
