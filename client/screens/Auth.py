import customtkinter as ctk

from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from network.Session import Session
from Store import Store
from Theme import Theme
from Widgets import FormField, MenuButton, SectionTitle


class Auth(ctk.CTkFrame):
    # Entry screen for sign-in and account registration.

    def __init__(self, master, navigator, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.navigator = navigator

        self.grid_columnconfigure(0, weight=1)

        self.BuildHeader()
        self.BuildForm()

    def BuildHeader(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        SectionTitle(header, "people", Locale.t("account.login.title")).grid(
            row=0,
            column=0,
            sticky=Layout.Sticky(),
        )

        Layout.Label(
            header,
            text=Locale.t("account.login.subtitle"),
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        ).grid(row=1, column=0, sticky=Layout.Sticky(), pady=(6, 0))

        divider = ctk.CTkFrame(self, height=1, fg_color=Theme.BorderSoft)
        divider.grid(row=1, column=0, sticky="ew", pady=(18, 0))
        divider.grid_propagate(False)

    def BuildForm(self) -> None:
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        form.grid_columnconfigure(0, weight=1)

        self.login = FormField(
            form,
            Locale.t("account.login.identifier"),
            Locale.t("account.login.identifier.placeholder"),
        )
        self.login.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.password = FormField(
            form,
            Locale.t("account.password"),
            Locale.t("account.password.placeholder"),
            show="*",
        )
        self.password.grid(row=1, column=0, sticky="ew", pady=(0, 16))

        MenuButton(
            form,
            icon="play",
            label=Locale.t("account.login.button"),
            command=self.OnLogin,
            variant="accent",
        ).grid(row=2, column=0, sticky="ew", pady=(0, 8))

        MenuButton(
            form,
            icon="people",
            label=Locale.t("account.login.create"),
            command=self.OnRegister,
            variant="primary",
        ).grid(row=3, column=0, sticky="ew")

    def OnRegister(self) -> None:
        self.navigator.ShowRegister()

    def OnLogin(self) -> None:
        login = self.login.Get()
        password = self.password.Get()

        if not login or not password:
            self.navigator.ShowNotice(
                Locale.t("account.error.login"),
                Locale.t("account.error.credentials_required"),
                success=False,
            )
            return

        success, result = Session.LoginUser(login, password)

        if not success:
            message = result if isinstance(result, str) else Locale.t("account.error.login")
            self.navigator.ShowNotice(Locale.t("account.error.login"), message, success=False)
            return

        if not isinstance(result, dict):
            self.navigator.ShowNotice(
                Locale.t("account.error.login"),
                Locale.t("account.error.login"),
                success=False,
            )
            return

        Store.SaveUser(result)

        if Store.Active:
            self.navigator.ShowMenu()
            return

        self.navigator.ShowVerifyEmail()
