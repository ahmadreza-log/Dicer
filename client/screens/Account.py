import customtkinter as ctk

from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from Store import Store
from Theme import Theme
from Widgets import BackButton, MenuButton, SectionTitle


class Account(ctk.CTkFrame):
    # Account hub for registration and email verification.

    def __init__(self, master, navigator, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.navigator = navigator

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.BuildHeader()
        self.BuildPanel()

    def Refresh(self) -> None:
        for widget in self.status_panel.winfo_children():
            widget.destroy()

        if Store.UserId and Store.Active:
            self.status_panel.grid()
            Layout.Label(
                self.status_panel,
                text=Locale.t("account.status.verified", username=Store.Username, email=Store.Email),
                font=Fonts.Body(),
                text_color=Theme.Text,
            ).pack(anchor=Layout.Anchor())
            self.register_button.grid_remove()
            self.verify_button.grid_remove()
            self.logout_button.grid(row=1, column=0, sticky="ew", pady=5)
            return

        self.logout_button.grid_remove()

        if Store.UserId:
            self.status_panel.grid()
            Layout.Label(
                self.status_panel,
                text=Locale.t("account.status.pending", email=Store.Email),
                font=Fonts.Body(),
                text_color=Theme.TextMuted,
            ).pack(anchor=Layout.Anchor())
            self.register_button.grid_remove()
            self.verify_button.grid()
            return

        self.status_panel.grid_remove()
        self.register_button.grid()
        self.verify_button.grid_remove()

    def BuildHeader(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        back = BackButton(header, command=self.OnBack)
        titles = ctk.CTkFrame(header, fg_color="transparent")
        Layout.PlaceScreenHeader(back, titles)

        SectionTitle(titles, "people", Locale.t("account.title")).grid(
            row=0,
            column=0,
            sticky=Layout.Sticky(),
        )

        Layout.Label(
            titles,
            text=Locale.t("account.subtitle"),
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        ).grid(row=1, column=0, sticky=Layout.Sticky(), pady=(6, 0))

        divider = ctk.CTkFrame(self, height=1, fg_color=Theme.BorderSoft)
        divider.grid(row=1, column=0, sticky="ew", pady=(18, 0))
        divider.grid_propagate(False)

    def BuildPanel(self) -> None:
        panel = ctk.CTkFrame(self, fg_color="transparent")
        panel.grid(row=2, column=0, sticky="nsew", pady=(20, 0))
        panel.grid_columnconfigure(0, weight=1)

        self.status_panel = ctk.CTkFrame(panel, fg_color=Theme.SurfaceRaised, corner_radius=Theme.RadiusSmall)
        self.status_panel.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        self.status_panel.grid_remove()

        self.register_button = MenuButton(
            panel,
            icon="play",
            label=Locale.t("account.register.button"),
            command=self.OnRegister,
            variant="accent",
        )
        self.register_button.grid(row=1, column=0, sticky="ew", pady=5)

        self.verify_button = MenuButton(
            panel,
            icon="bolt",
            label=Locale.t("account.verify.button"),
            command=self.OnVerify,
            variant="primary",
        )
        self.verify_button.grid(row=2, column=0, sticky="ew", pady=5)
        self.verify_button.grid_remove()

        self.logout_button = MenuButton(
            panel,
            icon="door",
            label=Locale.t("account.logout.button"),
            command=self.OnLogout,
            variant="danger",
        )
        self.logout_button.grid(row=3, column=0, sticky="ew", pady=5)
        self.logout_button.grid_remove()

    def OnBack(self) -> None:
        self.navigator.GoBack()

    def OnRegister(self) -> None:
        self.navigator.ShowRegister()

    def OnVerify(self) -> None:
        self.navigator.ShowVerifyEmail()

    def OnLogout(self) -> None:
        self.navigator.Logout()
