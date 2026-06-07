import customtkinter as ctk

from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from Theme import Theme
from Widgets import MenuButton


class Notice(ctk.CTkFrame):
    # Simple result screen after connect or other async actions.

    def __init__(
        self,
        master,
        navigator,
        title: str,
        message: str,
        success: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.navigator = navigator
        self.title = title
        self.message = message
        self.success = success

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.Build()

    def Build(self) -> None:
        icon = "✓" if self.success else "✕"
        color = Theme.Accent if self.success else Theme.Danger

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")

        Layout.Label(
            header,
            text=icon,
            font=Fonts.Make(42, "bold"),
            text_color=color,
        ).pack(anchor=Layout.Anchor())

        Layout.Label(
            header,
            text=self.title,
            font=Fonts.Heading(),
            text_color=Theme.Text,
        ).pack(anchor=Layout.Anchor(), pady=(12, 0))

        Layout.Label(
            header,
            text=self.message,
            font=Fonts.Body(),
            text_color=Theme.TextMuted,
            wraplength=640,
        ).pack(anchor=Layout.Anchor(), pady=(10, 0))

        divider = ctk.CTkFrame(self, height=1, fg_color=Theme.BorderSoft)
        divider.grid(row=1, column=0, sticky="ew", pady=(24, 0))
        divider.grid_propagate(False)

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="ew", pady=(24, 0))
        actions.grid_columnconfigure(0, weight=1)

        MenuButton(
            actions,
            icon="play" if self.success else "door",
            label=Locale.t("notice.back_menu"),
            command=self.OnBack,
            variant="accent" if self.success else "primary",
        ).grid(row=0, column=0, sticky="ew")

    def OnBack(self) -> None:
        self.navigator.ShowMenu()
