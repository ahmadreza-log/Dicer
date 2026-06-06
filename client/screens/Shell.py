import customtkinter as ctk

from Fonts import Fonts
from Theme import Theme
from Widgets import SectionTitle


class Shell(ctk.CTkFrame):
    # Shared chrome with a full-width expanded content card for inner screens.

    def __init__(self, master, navigator, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.navigator = navigator
        self.active: ctk.CTkFrame | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.BuildHeader()
        self.BuildContent()

    def BuildHeader(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 8))
        header.grid_columnconfigure(0, weight=1)

        accent = ctk.CTkFrame(header, height=3, fg_color=Theme.Accent, corner_radius=2)
        accent.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        accent.grid_propagate(False)

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.grid(row=1, column=0, sticky="ew")
        title_row.grid_columnconfigure(0, weight=1)

        SectionTitle(title_row, "dice", "Dicer", icon_size=34, font=Fonts.Title()).grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            title_row,
            text="  CLIENT  ",
            font=Fonts.Caption(),
            text_color=Theme.Accent,
            fg_color=Theme.AccentMuted,
            corner_radius=6,
        ).grid(row=0, column=1, sticky="e", padx=(12, 0))

        ctk.CTkLabel(
            header,
            text="Your tabletop hub — pick an action below",
            font=Fonts.Subtitle(),
            text_color=Theme.TextMuted,
        ).grid(row=2, column=0, sticky="w", pady=(8, 0))

    def BuildContent(self) -> None:
        self.card = ctk.CTkFrame(
            self,
            fg_color=Theme.Surface,
            corner_radius=Theme.Radius,
            border_width=1,
            border_color=Theme.Border,
        )
        self.card.grid(row=1, column=0, sticky="nsew", padx=32, pady=(8, 28))
        self.card.grid_columnconfigure(0, weight=1)
        self.card.grid_rowconfigure(0, weight=1)

        self.stage = ctk.CTkFrame(self.card, fg_color="transparent")
        self.stage.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
        self.stage.grid_columnconfigure(0, weight=1)
        self.stage.grid_rowconfigure(0, weight=1)

    def Show(self, screen: ctk.CTkFrame) -> None:
        if self.active is not None:
            self.active.grid_forget()

        self.active = screen
        screen.grid(row=0, column=0, sticky="nsew")
