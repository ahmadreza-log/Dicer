import customtkinter as ctk

from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from Theme import Theme
from Widgets import MenuButton


class CampaignPicker(ctk.CTkToplevel):
    # Popup listing saved campaigns with an option to create a new one.

    Width = 460
    Height = 420

    def __init__(self, parent, campaigns: list[dict], on_select, on_create) -> None:
        super().__init__(parent)

        self.on_select = on_select
        self.on_create = on_create
        self.campaigns = campaigns

        self.title(Locale.t("campaign.picker.window"))
        self.geometry(f"{self.Width}x{self.Height}")
        self.resizable(False, False)
        self.configure(fg_color=Theme.Surface)
        self.transient(parent)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.Build()
        self.Center(parent)

    def Build(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 12))
        header.grid_columnconfigure(0, weight=1)

        Layout.Label(
            header,
            text=Locale.t("campaign.picker.title"),
            font=Fonts.Heading(),
            text_color=Theme.Text,
        ).grid(row=0, column=0, sticky=Layout.Sticky())

        Layout.Label(
            header,
            text=Locale.t("campaign.picker.subtitle"),
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        ).grid(row=1, column=0, sticky=Layout.Sticky(), pady=(6, 0))

        list_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=Theme.SurfaceRaised,
            border_width=1,
            border_color=Theme.Border,
            corner_radius=Theme.RadiusSmall,
        )
        list_frame.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 12))
        list_frame.grid_columnconfigure(0, weight=1)

        for index, campaign in enumerate(self.campaigns):
            self.BuildCampaignRow(list_frame, campaign, index)

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 24))
        actions.grid_columnconfigure(0, weight=1)

        MenuButton(
            actions,
            icon="mage",
            label=Locale.t("campaign.picker.create"),
            command=self.OnCreate,
            variant="accent",
        ).grid(row=0, column=0, sticky="ew")

    def BuildCampaignRow(self, parent, campaign: dict, index: int) -> None:
        visibility = (
            Locale.t("campaign.visibility.private")
            if campaign.get("private")
            else Locale.t("campaign.visibility.public")
        )
        players = Locale.t("campaign.list.players", count=campaign.get("capacity", 0))
        label = f"{campaign.get('name', 'Campaign')}  ·  {players}  ·  {visibility}"

        button = ctk.CTkButton(
            parent,
            text=label,
            anchor=Layout.ButtonAnchor(),
            height=46,
            corner_radius=Theme.RadiusSmall,
            fg_color=Theme.Background,
            hover_color=Theme.AccentMuted,
            border_width=1,
            border_color=Theme.Border,
            text_color=Theme.Text,
            font=Fonts.Body(),
            command=lambda value=campaign: self.OnSelect(value),
        )
        button.grid(row=index, column=0, sticky="ew", pady=4)

    def Center(self, parent) -> None:
        self.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        x = parent_x + (parent_w - self.Width) // 2
        y = parent_y + (parent_h - self.Height) // 2
        self.geometry(f"{self.Width}x{self.Height}+{x}+{y}")

    def OnSelect(self, campaign: dict) -> None:
        self.grab_release()
        self.destroy()
        self.on_select(campaign)

    def OnCreate(self) -> None:
        self.grab_release()
        self.destroy()
        self.on_create()
