import customtkinter as ctk

from Fonts import Fonts
from network.Session import Session
from Theme import Theme
from Widgets import BackButton, RoleButton, SectionTitle


class Start(ctk.CTkFrame):
    # Role selection shown after the user presses Start on the main menu.

    Roles = (
        ("shield", "I am a ", "Dungeon Master", "dm"),
        ("swords", "I want an ", "Adventure", "adventure"),
        ("eye", "I just want to ", "Watch", "watch"),
    )

    def __init__(self, master, navigator, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.navigator = navigator

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.BuildHeader()
        self.BuildButtons()

    def BuildHeader(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        BackButton(header, command=self.OnBack).grid(row=0, column=0, sticky="w")

        titles = ctk.CTkFrame(header, fg_color="transparent")
        titles.grid(row=0, column=1, sticky="w", padx=(16, 0))
        titles.grid_columnconfigure(0, weight=1)

        SectionTitle(titles, "play", "Start").grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            titles,
            text="How do you want to join the session?",
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        divider = ctk.CTkFrame(self, height=1, fg_color=Theme.BorderSoft)
        divider.grid(row=1, column=0, sticky="ew", pady=(18, 0))
        divider.grid_propagate(False)

    def BuildButtons(self) -> None:
        panel = ctk.CTkFrame(self, fg_color="transparent")
        panel.grid(row=2, column=0, sticky="nsew", pady=(20, 0))
        panel.grid_columnconfigure(0, weight=1)

        for row, (icon, prefix, highlight, role) in enumerate(self.Roles):
            RoleButton(
                panel,
                icon=icon,
                prefix=prefix,
                highlight=highlight,
                command=lambda value=role: self.OnRole(value),
            ).grid(row=row, column=0, sticky="ew", pady=6)

    def OnBack(self) -> None:
        self.navigator.ShowMenu()

    def OnRole(self, role: str) -> None:
        if role != "dm":
            return

        success, message = Session.Register(role)

        if success:
            self.navigator.ShowNotice(
                "Connected",
                f"You are registered as {message}.\n"
                "Your connection is visible in the server management panel.",
                success=True,
            )
            return

        self.navigator.ShowNotice("Connection Failed", message, success=False)
