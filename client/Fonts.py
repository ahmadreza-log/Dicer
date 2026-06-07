import ctypes
import sys
from pathlib import Path

import customtkinter as ctk

from i18n.Locale import Locale


class Fonts:
    # Loads bundled font files and exposes locale-aware CTkFont presets.

    LatinFamily = "Inter"
    PersianFamily = "IRANSansDN"
    Fallback = "Segoe UI"
    Loaded = False

    Assets = Path(__file__).resolve().parent / "assets" / "fonts"
    Files = {
        "Iransansdn-Regular.ttf": PersianFamily,
    }

    @classmethod
    def Load(cls) -> None:
        if cls.Loaded:
            return

        if cls.Assets.is_dir():
            for path in sorted(cls.Assets.glob("*.ttf")):
                cls.Register(path)

        cls.Loaded = True

    @classmethod
    def Register(cls, path: Path) -> None:
        if sys.platform != "win32":
            return

        flag = 0x10  # FR_PRIVATE — available to this process only
        ctypes.windll.gdi32.AddFontResourceExW(str(path.resolve()), flag, 0)

    @classmethod
    def Family(cls) -> str:
        if Locale.Code == "fa":
            return cls.PersianFamily

        return cls.LatinFamily

    @classmethod
    def Make(cls, size: int, weight: str = "normal") -> ctk.CTkFont:
        if Locale.IsRtl() and weight == "bold":
            weight = "normal"

        return ctk.CTkFont(family=cls.Family(), size=size, weight=weight)

    @classmethod
    def Title(cls) -> ctk.CTkFont:
        return cls.Make(34, "bold")

    @classmethod
    def Subtitle(cls) -> ctk.CTkFont:
        return cls.Make(14)

    @classmethod
    def Heading(cls) -> ctk.CTkFont:
        return cls.Make(20, "bold")

    @classmethod
    def Body(cls) -> ctk.CTkFont:
        return cls.Make(14)

    @classmethod
    def Caption(cls) -> ctk.CTkFont:
        return cls.Make(12)

    @classmethod
    def Button(cls) -> ctk.CTkFont:
        return cls.Make(15, "normal")

    @classmethod
    def ButtonBold(cls) -> ctk.CTkFont:
        return cls.Make(15, "bold")
