import customtkinter as ctk

from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from network.Session import Session
from Store import Store
from Theme import Theme
from Widgets import BackButton, FormField, MenuButton, SectionTitle


class VerifyEmail(ctk.CTkFrame):
    # In-app email verification using a 6-digit activation code.

    def __init__(self, master, navigator, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.navigator = navigator

        self.grid_columnconfigure(0, weight=1)

        self.BuildHeader()
        self.BuildForm()

    def Refresh(self) -> None:
        email = Store.Email or Locale.t("account.email.placeholder")
        self.hint.configure(
            text=Locale.t("account.verify.subtitle", email=email),
            anchor=Layout.Anchor(),
            justify=Layout.Justify(),
        )

    def BuildHeader(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        back = BackButton(header, command=self.OnBack)
        titles = ctk.CTkFrame(header, fg_color="transparent")
        Layout.PlaceScreenHeader(back, titles)

        SectionTitle(titles, "bolt", Locale.t("account.verify.title")).grid(
            row=0,
            column=0,
            sticky=Layout.Sticky(),
        )

        self.hint = Layout.Label(
            titles,
            text=Locale.t("account.verify.subtitle", email=Store.Email or "—"),
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        )
        self.hint.grid(row=1, column=0, sticky=Layout.Sticky(), pady=(6, 0))

        divider = ctk.CTkFrame(self, height=1, fg_color=Theme.BorderSoft)
        divider.grid(row=1, column=0, sticky="ew", pady=(18, 0))
        divider.grid_propagate(False)

    def BuildForm(self) -> None:
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        form.grid_columnconfigure(0, weight=1)

        self.code = FormField(
            form,
            Locale.t("account.verify.code"),
            Locale.t("account.verify.code.placeholder"),
        )
        self.code.grid(row=0, column=0, sticky="ew", pady=(0, 16))

        MenuButton(
            form,
            icon="play",
            label=Locale.t("account.verify.button"),
            command=self.OnVerify,
            variant="accent",
        ).grid(row=1, column=0, sticky="ew", pady=(0, 8))

        MenuButton(
            form,
            icon="bolt",
            label=Locale.t("account.verify.resend"),
            command=self.OnResend,
            variant="primary",
        ).grid(row=2, column=0, sticky="ew")

    def OnBack(self) -> None:
        if self.navigator.IsAuthenticated():
            self.navigator.ShowAccount()
            return

        self.navigator.ShowAuth()

    def OnVerify(self) -> None:
        code = self.code.Get()

        if not code:
            self.navigator.ShowNotice(
                Locale.t("account.error.verify"),
                Locale.t("account.error.code_required"),
                success=False,
            )
            return

        if not Store.UserId:
            self.navigator.ShowNotice(
                Locale.t("account.error.verify"),
                Locale.t("account.error.no_user"),
                success=False,
            )
            return

        success, result = Session.VerifyEmail(Store.UserId, code)

        if not success:
            message = result if isinstance(result, str) else Locale.t("account.error.verify")
            self.navigator.ShowNotice(Locale.t("account.error.verify"), message, success=False)
            return

        if isinstance(result, dict):
            Store.SaveUser(result)

        if self.navigator.IsAuthenticated():
            self.navigator.ShowMenu()
            return

        self.navigator.ShowNotice(
            Locale.t("account.verify.success.title"),
            Locale.t("account.verify.success.body"),
            success=True,
        )

    def OnResend(self) -> None:
        if not Store.UserId:
            self.navigator.ShowNotice(
                Locale.t("account.error.verify"),
                Locale.t("account.error.no_user"),
                success=False,
            )
            return

        success, message = Session.ResendActivation(Store.UserId)

        if not success:
            self.navigator.ShowNotice(
                Locale.t("account.error.verify"),
                message,
                success=False,
            )
            return

        self.navigator.ShowNotice(
            Locale.t("account.verify.resent.title"),
            Locale.t("account.verify.resent.body"),
            success=True,
        )
