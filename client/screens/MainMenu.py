import customtkinter as ctk

from Fonts import Fonts
from network.Session import Session
from Theme import Theme
from Widgets import MenuButton, SectionTitle


class MainMenu(ctk.CTkFrame):
    # Primary navigation screen inside the expanded content card.

    Items = (
        ("accent", "play", "Start", "Connect to the server and begin"),
        ("primary", "house", "Rooms", "Browse and join game rooms"),
        ("primary", "mage", "Characters", "Manage your characters"),
        ("primary", "people", "Online Players", "See who is connected"),
        ("primary", "bolt", "Settings", "Client preferences and network"),
        ("danger", "door", "Exit", "Close the application"),
    )

    Handlers = {
        "Start": "OnStart",
        "Rooms": "OnRooms",
        "Characters": "OnCharacters",
        "Online Players": "OnOnlinePlayers",
        "Settings": "OnSettings",
        "Exit": "OnExit",
    }

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
        header.grid_columnconfigure(0, weight=1)

        SectionTitle(header, "bolt", "Main Menu").grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text="Choose where you want to go",
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

        for row, (variant, icon, label, _hint) in enumerate(self.Items):
            handler = getattr(self, self.Handlers[label])
            MenuButton(
                panel,
                icon=icon,
                label=label,
                command=handler,
                variant=variant,
            ).grid(row=row, column=0, sticky="ew", pady=5)

    def OnStart(self) -> None:
        success, message = Session.Connect()

        if not success:
            self.navigator.ShowNotice("Connection Failed", message, success=False)
            return

        self.navigator.ShowStart()

    def OnRooms(self) -> None:
        pass

    def OnCharacters(self) -> None:
        pass

    def OnOnlinePlayers(self) -> None:
        pass

    def OnSettings(self) -> None:
        self.navigator.ShowSettings()

    def OnExit(self) -> None:
        self.winfo_toplevel().destroy()
