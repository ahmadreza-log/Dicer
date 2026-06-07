import customtkinter as ctk

from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from Theme import Theme
from Widgets import BackButton, MenuButton, SectionTitle


class SettingsMenu(ctk.CTkFrame):
    # Settings hub with links to individual setting categories.

    Items = (
        ("house", "settings.network", "settings.network.hint", "OnNetwork"),
        ("bolt", "settings.language", "settings.language.hint", "OnLanguage"),
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

        back = BackButton(header, command=self.OnBack)
        titles = ctk.CTkFrame(header, fg_color="transparent")
        Layout.PlaceScreenHeader(back, titles)

        SectionTitle(titles, "bolt", Locale.t("settings.title")).grid(row=0, column=0, sticky=Layout.Sticky())

        Layout.Label(
            titles,
            text=Locale.t("settings.subtitle"),
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        ).grid(row=1, column=0, sticky=Layout.Sticky(), pady=(6, 0))

        divider = ctk.CTkFrame(self, height=1, fg_color=Theme.BorderSoft)
        divider.grid(row=1, column=0, sticky="ew", pady=(18, 0))
        divider.grid_propagate(False)

    def BuildButtons(self) -> None:
        panel = ctk.CTkFrame(self, fg_color="transparent")
        panel.grid(row=2, column=0, sticky="nsew", pady=(20, 0))
        panel.grid_columnconfigure(0, weight=1)

        for row, (icon, label_key, _hint_key, handler_name) in enumerate(self.Items):
            handler = getattr(self, handler_name)
            MenuButton(
                panel,
                icon=icon,
                label=Locale.t(label_key),
                command=handler,
                variant="primary",
            ).grid(row=row, column=0, sticky="ew", pady=5)

    def OnBack(self) -> None:
        self.navigator.ShowMenu()

    def OnNetwork(self) -> None:
        self.navigator.ShowNetwork()

    def OnLanguage(self) -> None:
        self.navigator.ShowLanguage()
