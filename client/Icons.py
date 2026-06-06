from pathlib import Path

import customtkinter as ctk
from PIL import Image


class Icons:
    # Local Twemoji PNG assets — consistent colorful icons on every platform.

    Root = Path(__file__).resolve().parent / "assets" / "icons"

    Files = {
        "dice": "dice.png",
        "play": "play.png",
        "house": "house.png",
        "mage": "mage.png",
        "people": "people.png",
        "door": "door.png",
        "shield": "shield.png",
        "swords": "swords.png",
        "eye": "eye.png",
        "bolt": "bolt.png",
    }

    _Cache: dict[tuple[str, int], ctk.CTkImage] = {}

    @classmethod
    def Get(cls, name: str, size: int = 24) -> ctk.CTkImage | None:
        key = (name, size)
        if key in cls._Cache:
            return cls._Cache[key]

        filename = cls.Files.get(name)
        if filename is None:
            return None

        path = cls.Root / filename
        if not path.is_file():
            return None

        source = Image.open(path)
        image = ctk.CTkImage(light_image=source, dark_image=source, size=(size, size))
        cls._Cache[key] = image
        return image
