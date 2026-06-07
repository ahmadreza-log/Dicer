import customtkinter as ctk

from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from network.Session import Session
from Store import Store
from Theme import Theme
from Widgets import BackButton, FormField, MenuButton, SectionTitle


class Register(ctk.CTkFrame):
    # Account registration with email verification follow-up.

    def __init__(self, master, navigator, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.navigator = navigator

        self.grid_columnconfigure(0, weight=1)

        self.BuildHeader()
        self.BuildForm()

    def BuildHeader(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        back = BackButton(header, command=self.OnBack)
        titles = ctk.CTkFrame(header, fg_color="transparent")
        Layout.PlaceScreenHeader(back, titles)

        SectionTitle(titles, "people", Locale.t("account.register.title")).grid(
            row=0,
            column=0,
            sticky=Layout.Sticky(),
        )

        Layout.Label(
            titles,
            text=Locale.t("account.register.subtitle"),
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

        self.username = FormField(
            form,
            Locale.t("account.username"),
            Locale.t("account.username.placeholder"),
        )
        self.username.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.email = FormField(
            form,
            Locale.t("account.email"),
            Locale.t("account.email.placeholder"),
        )
        self.email.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        self.password = FormField(
            form,
            Locale.t("account.password"),
            Locale.t("account.password.placeholder"),
            show="*",
        )
        self.password.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        self.confirm = FormField(
            form,
            Locale.t("account.password_confirm"),
            Locale.t("account.password_confirm.placeholder"),
            show="*",
        )
        self.confirm.grid(row=3, column=0, sticky="ew", pady=(0, 16))

        MenuButton(
            form,
            icon="play",
            label=Locale.t("account.register.button"),
            command=self.OnSubmit,
            variant="accent",
        ).grid(row=4, column=0, sticky="ew")

    def OnBack(self) -> None:
        self.navigator.GoBack()

    def OnSubmit(self) -> None:
        username = self.username.Get()
        email = self.email.Get()
        password = self.password.Get()
        confirm = self.confirm.Get()

        if password != confirm:
            self.navigator.ShowNotice(
                Locale.t("account.error.register"),
                Locale.t("account.error.password_mismatch"),
                success=False,
            )
            return

        success, result = Session.RegisterUser(username, email, password)

        if not success:
            message = result if isinstance(result, str) else Locale.t("account.error.register")
            self.navigator.ShowNotice(Locale.t("account.error.register"), message, success=False)
            return

        if not isinstance(result, dict):
            self.navigator.ShowNotice(
                Locale.t("account.error.register"),
                Locale.t("account.error.register"),
                success=False,
            )
            return

        Store.SaveUser(result)
        self.navigator.ShowVerifyEmail()
