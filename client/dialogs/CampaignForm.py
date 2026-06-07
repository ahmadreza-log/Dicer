import customtkinter as ctk

from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from Theme import Theme
from Widgets import FormField, MenuButton


class CampaignForm(ctk.CTkToplevel):
    # Popup form for creating a new campaign template.

    Width = 460
    Height = 520

    def __init__(self, parent, on_submit, on_cancel=None) -> None:
        super().__init__(parent)

        self.on_submit = on_submit
        self.on_cancel = on_cancel

        self.title(Locale.t("campaign.form.window"))
        self.geometry(f"{self.Width}x{self.Height}")
        self.resizable(False, False)
        self.configure(fg_color=Theme.Surface)
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.OnCancel)

        self.grid_columnconfigure(0, weight=1)

        self.Build()
        self.Center(parent)

    def Build(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 12))
        header.grid_columnconfigure(0, weight=1)

        Layout.Label(
            header,
            text=Locale.t("campaign.form.title"),
            font=Fonts.Heading(),
            text_color=Theme.Text,
        ).grid(row=0, column=0, sticky=Layout.Sticky())

        Layout.Label(
            header,
            text=Locale.t("campaign.form.subtitle"),
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
            wraplength=380,
        ).grid(row=1, column=0, sticky=Layout.Sticky(), pady=(6, 0))

        form = ctk.CTkFrame(self, fg_color="transparent")
        form.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 12))
        form.grid_columnconfigure(0, weight=1)

        self.name = FormField(
            form,
            Locale.t("campaign.form.name"),
            Locale.t("campaign.form.name.placeholder"),
        )
        self.name.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.capacity = FormField(
            form,
            Locale.t("campaign.form.capacity"),
            Locale.t("campaign.form.capacity.placeholder"),
        )
        self.capacity.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        private_row = ctk.CTkFrame(form, fg_color="transparent")
        private_row.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        self.private = ctk.CTkCheckBox(
            private_row,
            text=Locale.t("campaign.form.private"),
            font=Fonts.Body(),
            text_color=Theme.Text,
            fg_color=Theme.Accent,
            hover_color=Theme.AccentHover,
            border_color=Theme.Border,
        )
        self.private.pack(anchor=Layout.Anchor())

        self.password = FormField(
            form,
            Locale.t("campaign.form.password"),
            Locale.t("campaign.form.password.placeholder"),
        )
        self.password.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 24))
        actions.grid_columnconfigure((0, 1), weight=1)

        MenuButton(
            actions,
            icon="door",
            label=Locale.t("common.cancel"),
            command=self.OnCancel,
            variant="primary",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        MenuButton(
            actions,
            icon="play",
            label=Locale.t("campaign.form.create"),
            command=self.OnSubmit,
            variant="accent",
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

    def Center(self, parent) -> None:
        self.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        x = parent_x + (parent_w - self.Width) // 2
        y = parent_y + (parent_h - self.Height) // 2
        self.geometry(f"{self.Width}x{self.Height}+{x}+{y}")

    def OnCancel(self) -> None:
        self.grab_release()
        self.destroy()

        if self.on_cancel:
            self.on_cancel()

    def OnSubmit(self) -> None:
        name = self.name.Get()
        capacity_text = self.capacity.Get()
        private = bool(self.private.get())
        password = self.password.Get()

        if not name:
            self.ShowError(Locale.t("campaign.form.error.name_required"))
            return

        try:
            capacity = int(capacity_text)
        except ValueError:
            self.ShowError(Locale.t("campaign.form.error.capacity_number"))
            return

        if capacity <= 0:
            self.ShowError(Locale.t("campaign.form.error.capacity_positive"))
            return

        self.grab_release()
        self.destroy()
        self.on_submit(
            {
                "name": name,
                "capacity": capacity,
                "private": private,
                "password": password,
            }
        )

    def ShowError(self, message: str) -> None:
        existing = getattr(self, "_error", None)

        if existing is not None:
            existing.destroy()

        self._error = Layout.Label(
            self,
            text=message,
            font=Fonts.Caption(),
            text_color=Theme.Danger,
        )
        self._error.grid(row=3, column=0, sticky=Layout.Sticky(), padx=24, pady=(0, 8))
