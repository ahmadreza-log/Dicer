import customtkinter as ctk

from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from network.Probe import Probe
from network.Session import Session
from Settings import Settings
from Store import Store
from Theme import Theme
from Widgets import BackButton, FormField, MenuButton, SectionTitle


class Network(ctk.CTkFrame):
    # Network settings — server IP destination (port is fixed on the server).

    def __init__(self, master, navigator, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.navigator = navigator

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.BuildHeader()
        self.BuildForm()

    def BuildHeader(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        back = BackButton(header, command=self.OnBack)
        titles = ctk.CTkFrame(header, fg_color="transparent")
        Layout.PlaceScreenHeader(back, titles)

        SectionTitle(titles, "house", Locale.t("network.title")).grid(row=0, column=0, sticky=Layout.Sticky())

        Layout.Label(
            titles,
            text=Locale.t("network.subtitle"),
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        ).grid(row=1, column=0, sticky=Layout.Sticky(), pady=(6, 0))

        divider = ctk.CTkFrame(self, height=1, fg_color=Theme.BorderSoft)
        divider.grid(row=1, column=0, sticky="ew", pady=(18, 0))
        divider.grid_propagate(False)

    def BuildForm(self) -> None:
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.grid(row=2, column=0, sticky="nsew", pady=(20, 0))
        form.grid_columnconfigure(0, weight=1)

        self.host = FormField(form, Locale.t("network.ip"), Locale.t("network.ip.placeholder"))
        self.host.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.port_label = Layout.Label(
            form,
            text=Locale.t("network.port_fixed", port=Settings.Port),
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        )
        self.port_label.grid(row=1, column=0, sticky=Layout.Sticky(), pady=(0, 8))

        self.target = Layout.Label(
            form,
            text=Locale.t("network.current_target", endpoint=Settings.Endpoint()),
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        )
        self.target.grid(row=2, column=0, sticky=Layout.Sticky(), pady=(4, 18))

        actions = ctk.CTkFrame(form, fg_color="transparent")
        actions.grid(row=3, column=0, sticky="ew")
        actions.grid_columnconfigure(0, weight=1)

        MenuButton(
            actions,
            icon="play",
            label=Locale.t("common.save"),
            command=self.OnSave,
            variant="accent",
        ).grid(row=0, column=0, sticky="ew", pady=5)

        MenuButton(
            actions,
            icon="shield",
            label=Locale.t("network.test"),
            command=self.OnTest,
            variant="primary",
        ).grid(row=1, column=0, sticky="ew", pady=5)

        self.LoadFields()

    def LoadFields(self) -> None:
        self.host.Set(Settings.Host)
        self.port_label.configure(
            text=Locale.t("network.port_fixed", port=Settings.Port),
            anchor=Layout.Anchor(),
            justify=Layout.Justify(),
        )
        self.target.configure(
            text=Locale.t("network.current_target", endpoint=Settings.Endpoint()),
            anchor=Layout.Anchor(),
            justify=Layout.Justify(),
        )

    def OnBack(self) -> None:
        self.navigator.ShowSettings()

    def OnSave(self) -> None:
        host = self.host.Get()
        valid, error = Settings.ValidateHost(host)

        if not valid:
            self.navigator.ShowNotice(Locale.t("network.invalid.title"), Locale.t(error), success=False)
            return

        Settings.ApplyHost(host)
        Session.Disconnect()
        saved, message = Store.Save()
        self.LoadFields()

        if not saved:
            detail = Locale.t(message) if message == "store.saved" else message
            self.navigator.ShowNotice(Locale.t("network.save_failed"), detail, success=False)
            return

        self.navigator.ShowNotice(
            Locale.t("network.saved.title"),
            Locale.t("network.saved.body", host=Settings.Host, port=Settings.Port),
            success=True,
        )

    def OnTest(self) -> None:
        host = self.host.Get()
        valid, error = Settings.ValidateHost(host)

        if not valid:
            self.navigator.ShowNotice(Locale.t("network.invalid.title"), Locale.t(error), success=False)
            return

        success, message = Probe.Test(host, Settings.Port)

        if success:
            self.navigator.ShowNotice(
                Locale.t("network.test.ok.title"),
                Locale.t("network.test.ok.body", endpoint=Settings.Endpoint(), message=message),
                success=True,
            )
            return

        self.navigator.ShowNotice(Locale.t("network.test.failed"), message, success=False)
