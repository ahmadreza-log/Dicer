import customtkinter as ctk

from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from network.Session import Session
from Theme import Theme
from Widgets import BackButton, FormField, MenuButton, SectionTitle


class JoinRoom(ctk.CTkFrame):
    # Room ID entry for players and spectators joining an existing session.

    Icons = {
        "adventure": "swords",
        "watch": "eye",
    }

    TitleKeys = {
        "adventure": "join.title.player",
        "watch": "join.title.spectator",
    }

    HintKeys = {
        "adventure": "join.hint.player",
        "watch": "join.hint.spectator",
    }

    def __init__(self, master, navigator, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.navigator = navigator
        self.role = "adventure"

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.BuildHeader()
        self.BuildForm()

    def Prepare(self, role: str) -> None:
        self.role = role
        icon = self.Icons.get(role, "house")
        title_key = self.TitleKeys.get(role, "join.title.player")
        hint_key = self.HintKeys.get(role, "join.hint.player")

        for widget in self.header_title.winfo_children():
            widget.destroy()

        SectionTitle(self.header_title, icon, Locale.t(title_key)).pack(anchor=Layout.Anchor())
        self.hint.configure(text=Locale.t(hint_key), anchor=Layout.Anchor(), justify=Layout.Justify())
        self.room_id.Set("")
        self.password.Set("")

    def BuildHeader(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        back = BackButton(header, command=self.OnBack)
        titles = ctk.CTkFrame(header, fg_color="transparent")
        titles.grid_columnconfigure(0, weight=1)
        Layout.PlaceScreenHeader(back, titles)

        self.header_title = ctk.CTkFrame(titles, fg_color="transparent")
        self.header_title.grid(row=0, column=0, sticky=Layout.Sticky())
        SectionTitle(self.header_title, "swords", Locale.t("join.title.player")).pack(anchor=Layout.Anchor())

        self.hint = Layout.Label(
            titles,
            text=Locale.t("join.hint.player"),
            font=Fonts.Caption(),
            text_color=Theme.TextDim,
        )
        self.hint.grid(row=1, column=0, sticky=Layout.Sticky(), pady=(6, 0))

        divider = ctk.CTkFrame(self, height=1, fg_color=Theme.BorderSoft)
        divider.grid(row=1, column=0, sticky="ew", pady=(18, 0))
        divider.grid_propagate(False)

    def BuildForm(self) -> None:
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.grid(row=2, column=0, sticky="nsew", pady=(20, 0))
        form.grid_columnconfigure(0, weight=1)

        self.room_id = FormField(
            form,
            Locale.t("join.room_id"),
            Locale.t("join.room_id.placeholder"),
        )
        self.room_id.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.password = FormField(
            form,
            Locale.t("join.password"),
            Locale.t("join.password.placeholder"),
        )
        self.password.grid(row=1, column=0, sticky="ew", pady=(0, 16))

        actions = ctk.CTkFrame(form, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="ew")
        actions.grid_columnconfigure(0, weight=1)

        MenuButton(
            actions,
            icon="play",
            label=Locale.t("join.button"),
            command=self.OnJoin,
            variant="accent",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 8))

    def OnBack(self) -> None:
        self.navigator.ShowStart()

    def OnJoin(self) -> None:
        room_id = self.room_id.Get()

        if not room_id:
            self.navigator.ShowNotice(
                Locale.t("join.error.room_required.title"),
                Locale.t("join.error.room_required.body"),
                success=False,
            )
            return

        success, message = Session.Register(
            self.role,
            room_id=room_id,
            password=self.password.Get(),
        )

        if not success:
            self.navigator.ShowNotice(Locale.t("join.error.failed"), message, success=False)
            return

        details = Locale.t("join.connected.body", role=message)
        room = Session.room

        if room:
            details += f"\n\n{Locale.t('start.connected.room_id', room_id=room['id'])}"

        self.navigator.ShowNotice(Locale.t("start.connected.title"), details, success=True)
