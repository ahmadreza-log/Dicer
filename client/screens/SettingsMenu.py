import customtkinter as ctk

from Fonts import Fonts
from Theme import Theme
from Widgets import BackButton, MenuButton, SectionTitle


class SettingsMenu(ctk.CTkFrame):
    # Settings hub with links to individual setting categories.

    Items = (
        ("house", "Network", "Set the server IP address"),
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

        SectionTitle(titles, "bolt", "Settings").grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            titles,
            text="Configure the client",
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

        for row, (icon, label, _hint) in enumerate(self.Items):
            MenuButton(
                panel,
                icon=icon,
                label=label,
                command=self.OnNetwork,
                variant="primary",
            ).grid(row=row, column=0, sticky="ew", pady=5)

    def OnBack(self) -> None:
        self.navigator.ShowMenu()

    def OnNetwork(self) -> None:
        self.navigator.ShowNetwork()
