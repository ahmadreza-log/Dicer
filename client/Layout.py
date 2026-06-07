import customtkinter as ctk

from i18n.Locale import Locale


class Layout:
    # Direction-aware layout helpers for LTR and RTL locales.

    @classmethod
    def IsRtl(cls) -> bool:
        return Locale.IsRtl()

    @classmethod
    def Anchor(cls) -> str:
        return "e" if cls.IsRtl() else "w"

    @classmethod
    def Justify(cls) -> str:
        return "right" if cls.IsRtl() else "left"

    @classmethod
    def Sticky(cls) -> str:
        return "e" if cls.IsRtl() else "w"

    @classmethod
    def ButtonAnchor(cls) -> str:
        return "e" if cls.IsRtl() else "w"

    @classmethod
    def Compound(cls) -> str:
        return "right" if cls.IsRtl() else "left"

    @classmethod
    def PackStart(cls) -> str:
        return "right" if cls.IsRtl() else "left"

    @classmethod
    def PackEnd(cls) -> str:
        return "left" if cls.IsRtl() else "right"

    @classmethod
    def HeaderBackColumn(cls) -> int:
        return 1 if cls.IsRtl() else 0

    @classmethod
    def HeaderTitleColumn(cls) -> int:
        return 0 if cls.IsRtl() else 1

    @classmethod
    def HeaderTitlePadx(cls) -> tuple[int, int]:
        return (0, 16) if cls.IsRtl() else (16, 0)

    @classmethod
    def Label(cls, master, **kwargs) -> ctk.CTkLabel:
        options = {
            "anchor": cls.Anchor(),
            "justify": cls.Justify(),
        }
        options.update(kwargs)
        return ctk.CTkLabel(master, **options)

    @classmethod
    def PlaceScreenHeader(cls, back_button, titles_frame) -> None:
        back_button.grid(
            row=0,
            column=Layout.HeaderBackColumn(),
            sticky=Layout.Sticky(),
        )
        titles_frame.grid(
            row=0,
            column=Layout.HeaderTitleColumn(),
            sticky=Layout.Sticky(),
            padx=Layout.HeaderTitlePadx(),
        )
