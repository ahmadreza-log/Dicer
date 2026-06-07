import customtkinter as ctk

from Fonts import Fonts


class Theme:
    # Visual tokens for the Dicer client — dark shell with teal accent.

    Mode = "dark"
    Color = "dark-blue"

    Accent = "#00bc8c"
    AccentHover = "#00d4a0"
    AccentMuted = "#0d3d34"

    Background = "#12151a"
    Surface = "#1a1f26"
    SurfaceRaised = "#222831"
    Border = "#2c333d"
    BorderSoft = "#232930"

    Text = "#eef2f7"
    TextMuted = "#8b949e"
    TextDim = "#6e7681"

    Danger = "#e5534b"
    DangerHover = "#ff6b63"
    DangerMuted = "#3d1f1f"

    Width = 980
    Height = 680
    MinWidth = 860
    MinHeight = 560
    MaxHeightRatio = 0.92

    Radius = 14
    RadiusSmall = 10

    @classmethod
    def Apply(cls) -> None:
        ctk.set_appearance_mode(cls.Mode)
        ctk.set_default_color_theme(cls.Color)
        Fonts.Load()
