import customtkinter as ctk

from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from network.Session import Session
from Theme import Theme
from Widgets import BackButton, FormField, SectionTitle


class Room(ctk.CTkFrame):
    # In-room chat shell shown after a successful register or join.

    def __init__(self, master, navigator, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.navigator = navigator

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.BuildHeader()
        self.BuildSettings()
        self.BuildChat()

    def Refresh(self) -> None:
        room = Session.room or {}
        role = Session.role or "guest"
        room_id = room.get("id", "")
        campaign_name = room.get("name") or room.get("campaign_name") or ""

        self._room_id = room_id
        self.room_id_box.configure(state="normal")
        self.room_id_box.delete(0, "end")
        self.room_id_box.insert(0, room_id or "—")
        self.room_id_box.configure(state="readonly")
        self.copy_button.configure(
            state="normal" if room_id else "disabled",
            text=Locale.t("room.id.copy"),
        )

        self.role_label.configure(text=Locale.t("room.role", role=Locale.t(f"role.{role}")))

        if campaign_name:
            self.campaign_label.configure(text=Locale.t("room.campaign", name=campaign_name))
            self.campaign_label.grid()
        else:
            self.campaign_label.grid_remove()

        if role == "dm":
            self.settings_panel.grid()
            visibility = str(room.get("visibility", "public")).lower()
            visibility_label = (
                Locale.t("campaign.visibility.private")
                if visibility == "private"
                else Locale.t("campaign.visibility.public")
            )
            password = str(room.get("password", "") or "")
            capacity = int(room.get("capacity", 0) or 0)
            players = int(room.get("players", 0) or 0)
            members = int(room.get("members", 0) or 0)

            self.SetReadOnly(self.settings_name, campaign_name or "—")
            self.SetReadOnly(self.settings_capacity, str(capacity) if capacity else "—")
            self.SetReadOnly(self.settings_visibility, visibility_label)
            self.SetReadOnly(
                self.settings_password,
                password if password else Locale.t("room.settings.password.none"),
            )
            self.SetReadOnly(
                self.settings_occupancy,
                Locale.t(
                    "room.settings.occupancy",
                    players=players,
                    members=members,
                    capacity=capacity,
                ),
            )
            return

        self.settings_panel.grid_remove()

    def SetReadOnly(self, field: FormField, value: str) -> None:
        field.input.configure(state="normal")
        field.Set(value)
        field.input.configure(state="readonly")

    def BuildSettings(self) -> None:
        panel = ctk.CTkFrame(self, fg_color=Theme.SurfaceRaised, corner_radius=Theme.RadiusSmall)
        panel.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_remove()
        self.settings_panel = panel

        SectionTitle(panel, "bolt", Locale.t("room.settings.title")).grid(
            row=0,
            column=0,
            sticky=Layout.Sticky(),
            padx=16,
            pady=(16, 12),
        )

        form = ctk.CTkFrame(panel, fg_color="transparent")
        form.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))
        form.grid_columnconfigure((0, 1), weight=1)

        self.settings_name = self.ReadOnlyField(
            form,
            Locale.t("room.settings.name"),
            row=0,
            column=0,
            padx=(0, 8),
            pady=(0, 10),
        )
        self.settings_capacity = self.ReadOnlyField(
            form,
            Locale.t("room.settings.capacity"),
            row=0,
            column=1,
            padx=(8, 0),
            pady=(0, 10),
        )
        self.settings_visibility = self.ReadOnlyField(
            form,
            Locale.t("room.settings.visibility"),
            row=1,
            column=0,
            padx=(0, 8),
            pady=(0, 10),
        )
        self.settings_password = self.ReadOnlyField(
            form,
            Locale.t("room.settings.password"),
            row=1,
            column=1,
            padx=(8, 0),
            pady=(0, 10),
        )
        self.settings_occupancy = self.ReadOnlyField(
            form,
            Locale.t("room.settings.occupancy.label"),
            row=2,
            column=0,
            columnspan=2,
            pady=(0, 0),
        )

    def ReadOnlyField(
        self,
        master,
        label: str,
        row: int,
        column: int,
        columnspan: int = 1,
        padx=0,
        pady=0,
    ) -> FormField:
        field = FormField(master, label, "")
        field.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="ew",
            padx=padx,
            pady=pady,
        )
        field.input.configure(state="readonly")
        return field

    def CopyRoomId(self) -> None:
        room_id = getattr(self, "_room_id", "")

        if not room_id:
            return

        window = self.winfo_toplevel()
        window.clipboard_clear()
        window.clipboard_append(room_id)
        window.update()

        self.copy_button.configure(text=Locale.t("room.id.copied"))
        self.after(1500, self.ResetCopyButton)

    def ResetCopyButton(self) -> None:
        if self.copy_button.winfo_exists():
            self.copy_button.configure(text=Locale.t("room.id.copy"))

    def LeaveRoom(self) -> None:
        self.leave_button.configure(state="disabled")
        self.back_button.configure(state="disabled")

        success, message = Session.LeaveRoom()

        if not success:
            self.leave_button.configure(state="normal")
            self.back_button.configure(state="normal")
            self.navigator.ShowNotice(Locale.t("room.leave.error"), message, success=False)
            return

        self.navigator.GoBack()

    def BuildHeader(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        self.back_button = BackButton(header, command=self.LeaveRoom)
        titles = ctk.CTkFrame(header, fg_color="transparent")
        titles.grid_columnconfigure(0, weight=1)
        Layout.PlaceScreenHeader(self.back_button, titles)

        title_row = ctk.CTkFrame(titles, fg_color="transparent")
        title_row.grid(row=0, column=0, sticky="ew")
        title_row.grid_columnconfigure(0, weight=1)

        SectionTitle(title_row, "house", Locale.t("room.title")).grid(
            row=0,
            column=0,
            sticky=Layout.Sticky(),
        )

        self.leave_button = ctk.CTkButton(
            title_row,
            text=Locale.t("room.leave"),
            command=self.LeaveRoom,
            width=120,
            height=36,
            font=Fonts.Button(),
            corner_radius=Theme.RadiusSmall,
            fg_color=Theme.Danger,
            hover_color=Theme.DangerHover,
        )
        self.leave_button.grid(row=0, column=1, sticky="e", padx=(12, 0))

        self.role_label = Layout.Label(
            header,
            text="",
            font=Fonts.Caption(),
            text_color=Theme.Accent,
        )
        self.role_label.grid(row=1, column=0, sticky=Layout.Sticky(), pady=(6, 0))

        self.room_id_row = ctk.CTkFrame(header, fg_color="transparent")
        self.room_id_row.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        self.room_id_row.grid_columnconfigure(1, weight=1)

        Layout.Label(
            self.room_id_row,
            text=Locale.t("room.id.label"),
            font=Fonts.Caption(),
            text_color=Theme.TextMuted,
        ).grid(row=0, column=0, sticky=Layout.Sticky(), padx=(0, 10))

        self.room_id_box = ctk.CTkEntry(
            self.room_id_row,
            height=42,
            font=Fonts.Button(),
            justify="center",
            corner_radius=Theme.RadiusSmall,
            border_color=Theme.Border,
            fg_color=Theme.SurfaceRaised,
        )
        self.room_id_box.grid(row=0, column=1, sticky="ew", padx=(0, 8))

        self.copy_button = ctk.CTkButton(
            self.room_id_row,
            text=Locale.t("room.id.copy"),
            command=self.CopyRoomId,
            width=96,
            height=42,
            font=Fonts.Button(),
            corner_radius=Theme.RadiusSmall,
            fg_color=Theme.SurfaceRaised,
            hover_color=Theme.AccentMuted,
            border_width=1,
            border_color=Theme.Border,
            text_color=Theme.Text,
        )
        self.copy_button.grid(row=0, column=2, sticky="e")

        self.campaign_label = Layout.Label(
            header,
            text="",
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        )
        self.campaign_label.grid(row=3, column=0, sticky=Layout.Sticky(), pady=(8, 0))

        divider = ctk.CTkFrame(self, height=1, fg_color=Theme.BorderSoft)
        divider.grid(row=1, column=0, sticky="ew", pady=(18, 0))
        divider.grid_propagate(False)

    def BuildChat(self) -> None:
        panel = ctk.CTkFrame(self, fg_color=Theme.SurfaceRaised, corner_radius=Theme.RadiusSmall)
        panel.grid(row=3, column=0, sticky="nsew", pady=(20, 0))
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1)

        self.messages = ctk.CTkTextbox(
            panel,
            font=Fonts.Body(),
            fg_color=Theme.Surface,
            border_width=1,
            border_color=Theme.Border,
            corner_radius=Theme.RadiusSmall,
            wrap="word",
            activate_scrollbars=True,
        )
        self.messages.grid(row=0, column=0, sticky="nsew", padx=16, pady=(16, 8))
        self.messages.configure(state="disabled")

        input_row = ctk.CTkFrame(panel, fg_color="transparent")
        input_row.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))
        input_row.grid_columnconfigure(0, weight=1)

        self.input = ctk.CTkEntry(
            input_row,
            placeholder_text=Locale.t("room.message.placeholder"),
            font=Fonts.Body(),
            height=42,
            corner_radius=Theme.RadiusSmall,
            border_color=Theme.Border,
            fg_color=Theme.Surface,
        )
        self.input.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.send = ctk.CTkButton(
            input_row,
            text=Locale.t("room.send"),
            font=Fonts.Button(),
            height=42,
            width=96,
            corner_radius=Theme.RadiusSmall,
            fg_color=Theme.Accent,
            hover_color=Theme.AccentHover,
            state="disabled",
        )
        self.send.grid(row=0, column=1)

        self.SetSystemMessage(Locale.t("room.placeholder"))

    def SetSystemMessage(self, message: str) -> None:
        self.messages.configure(state="normal")
        self.messages.delete("1.0", "end")
        self.messages.insert("1.0", message)
        self.messages.configure(state="disabled")
