import customtkinter as ctk


class Theme:
    # CustomTkinter appearance defaults for the Dicer client.

    Mode = "dark"
    Color = "green"
    Accent = "#00bc8c"
    Width = 960
    Height = 640
    MinWidth = 820
    MinHeight = 520

    @classmethod
    def Apply(cls) -> None:
        ctk.set_appearance_mode(cls.Mode)
        ctk.set_default_color_theme(cls.Color)
