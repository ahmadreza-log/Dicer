import customtkinter as ctk

from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from network.Session import Session
from Theme import Theme
from Widgets import MenuButton, SectionTitle


class MainMenu(ctk.CTkFrame):
    # Primary navigation screen inside the expanded content card.

    Items = (
        ("accent", "play", "menu.start", "OnStart"),
        ("primary", "house", "menu.rooms", "OnRooms"),
        ("primary", "mage", "menu.characters", "OnCharacters"),
        ("primary", "people", "menu.online_players", "OnOnlinePlayers"),
        ("primary", "bolt", "menu.settings", "OnSettings"),
        ("danger", "door", "menu.exit", "OnExit"),
    )

    def __init__(self, master, navigator, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.navigator = navigator

        self.grid_columnconfigure(0, weight=1)

        self.BuildHeader()
        self.BuildButtons()

    def BuildHeader(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        SectionTitle(header, "bolt", Locale.t("menu.title")).grid(row=0, column=0, sticky=Layout.Sticky())

        Layout.Label(
            header,
            text=Locale.t("menu.subtitle"),
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        ).grid(row=1, column=0, sticky=Layout.Sticky(), pady=(6, 0))

        divider = ctk.CTkFrame(self, height=1, fg_color=Theme.BorderSoft)
        divider.grid(row=1, column=0, sticky="ew", pady=(18, 0))
        divider.grid_propagate(False)

    def BuildButtons(self) -> None:
        panel = ctk.CTkFrame(self, fg_color="transparent")
        panel.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        panel.grid_columnconfigure(0, weight=1)

        for row, (variant, icon, label_key, handler_name) in enumerate(self.Items):
            handler = getattr(self, handler_name)
            MenuButton(
                panel,
                icon=icon,
                label=Locale.t(label_key),
                command=handler,
                variant=variant,
            ).grid(row=row, column=0, sticky="ew", pady=5)

    def OnStart(self) -> None:
        success, message = Session.Connect()

        if not success:
            self.navigator.ShowNotice(Locale.t("start.error.connection"), message, success=False)
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
