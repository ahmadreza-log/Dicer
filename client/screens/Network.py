import customtkinter as ctk

from Fonts import Fonts
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

        BackButton(header, command=self.OnBack).grid(row=0, column=0, sticky="w")

        titles = ctk.CTkFrame(header, fg_color="transparent")
        titles.grid(row=0, column=1, sticky="w", padx=(16, 0))

        SectionTitle(titles, "house", "Network").grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            titles,
            text="Set the server IP address for all connections",
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        divider = ctk.CTkFrame(self, height=1, fg_color=Theme.BorderSoft)
        divider.grid(row=1, column=0, sticky="ew", pady=(18, 0))
        divider.grid_propagate(False)

    def BuildForm(self) -> None:
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.grid(row=2, column=0, sticky="nsew", pady=(20, 0))
        form.grid_columnconfigure(0, weight=1)

        self.host = FormField(form, "IP Address", "127.0.0.1")
        self.host.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(
            form,
            text=f"Port: {Settings.Port} (fixed)",
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        ).grid(row=1, column=0, sticky="w", pady=(0, 8))

        self.target = ctk.CTkLabel(
            form,
            text=f"Current target: {Settings.Endpoint()}",
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        )
        self.target.grid(row=2, column=0, sticky="w", pady=(4, 18))

        actions = ctk.CTkFrame(form, fg_color="transparent")
        actions.grid(row=3, column=0, sticky="ew")
        actions.grid_columnconfigure(0, weight=1)

        MenuButton(
            actions,
            icon="play",
            label="Save",
            command=self.OnSave,
            variant="accent",
        ).grid(row=0, column=0, sticky="ew", pady=5)

        MenuButton(
            actions,
            icon="shield",
            label="Test Connection",
            command=self.OnTest,
            variant="primary",
        ).grid(row=1, column=0, sticky="ew", pady=5)

        self.LoadFields()

    def LoadFields(self) -> None:
        self.host.Set(Settings.Host)
        self.target.configure(text=f"Current target: {Settings.Endpoint()}")

    def OnBack(self) -> None:
        self.navigator.ShowSettings()

    def OnSave(self) -> None:
        host = self.host.Get()
        valid, error = Settings.ValidateHost(host)

        if not valid:
            self.navigator.ShowNotice("Invalid Settings", error, success=False)
            return

        Settings.ApplyHost(host)
        Session.Disconnect()
        saved, message = Store.Save()
        self.LoadFields()

        if not saved:
            self.navigator.ShowNotice("Save Failed", message, success=False)
            return

        self.navigator.ShowNotice(
            "Settings Saved",
            f"Server IP set to {Settings.Host} (port {Settings.Port}).",
            success=True,
        )

    def OnTest(self) -> None:
        host = self.host.Get()
        valid, error = Settings.ValidateHost(host)

        if not valid:
            self.navigator.ShowNotice("Invalid Settings", error, success=False)
            return

        success, message = Probe.Test(host, Settings.Port)

        if success:
            self.navigator.ShowNotice(
                "Connection OK",
                f"Reached {Settings.Endpoint()}\n{message}",
                success=True,
            )
            return

        self.navigator.ShowNotice("Connection Failed", message, success=False)
