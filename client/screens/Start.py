import customtkinter as ctk

from dialogs.CampaignForm import CampaignForm
from dialogs.CampaignPicker import CampaignPicker
from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from network.Session import Session
from Theme import Theme
from Widgets import BackButton, RoleButton, SectionTitle


class Start(ctk.CTkFrame):
    # Role selection shown after the user presses Start on the main menu.

    Roles = (
        ("shield", "start.role.dm.prefix", "start.role.dm.highlight", "dm"),
        ("swords", "start.role.adventure.prefix", "start.role.adventure.highlight", "adventure"),
        ("eye", "start.role.watch.prefix", "start.role.watch.highlight", "watch"),
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
        titles.grid_columnconfigure(0, weight=1)
        Layout.PlaceScreenHeader(back, titles)

        SectionTitle(titles, "play", Locale.t("start.title")).grid(row=0, column=0, sticky=Layout.Sticky())

        Layout.Label(
            titles,
            text=Locale.t("start.subtitle"),
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

        for row, (icon, prefix_key, highlight_key, role) in enumerate(self.Roles):
            RoleButton(
                panel,
                icon=icon,
                prefix=Locale.t(prefix_key),
                highlight=Locale.t(highlight_key),
                command=lambda value=role: self.OnRole(value),
            ).grid(row=row, column=0, sticky="ew", pady=6)

    def OnBack(self) -> None:
        self.navigator.ShowMenu()

    def OnRole(self, role: str) -> None:
        if role in ("adventure", "watch"):
            self.navigator.ShowJoinRoom(role)
            return

        if role != "dm":
            return

        self.OpenCampaignFlow()

    def OpenCampaignFlow(self) -> None:
        success, result = Session.ListCampaigns()
        campaigns = result if success and isinstance(result, list) else []

        if campaigns:
            CampaignPicker(
                self.winfo_toplevel(),
                campaigns,
                on_select=self.OnCampaignSelected,
                on_create=self.OpenCampaignForm,
            )
            return

        self.OpenCampaignForm()

    def OpenCampaignForm(self) -> None:
        CampaignForm(
            self.winfo_toplevel(),
            on_submit=self.OnCampaignCreated,
        )

    def OnCampaignSelected(self, campaign: dict) -> None:
        if not campaign.get("name"):
            self.navigator.ShowNotice(
                Locale.t("start.error.campaign"),
                Locale.t("start.error.invalid_campaign"),
                success=False,
            )
            return

        self.StartDungeonMaster(campaign)

    def OnCampaignCreated(self, data: dict) -> None:
        self.StartDungeonMaster(data)

    def RoomSettings(self, data: dict) -> dict:
        return {
            "name": data.get("name", ""),
            "capacity": data.get("capacity", 6),
            "private": bool(data.get("private", False)),
            "password": data.get("password", ""),
        }

    def StartDungeonMaster(self, campaign: dict) -> None:
        success, message = Session.Register("dm", room=self.RoomSettings(campaign))

        if not success:
            self.navigator.ShowNotice(Locale.t("start.error.connection"), message, success=False)
            return

        self.navigator.ShowRoom()
