import customtkinter as ctk

from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from Store import Store
from Theme import Theme
from Widgets import SectionTitle


class Shell(ctk.CTkFrame):
    # Shared chrome with a full-width expanded content card for inner screens.

    def __init__(self, master, navigator, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.navigator = navigator
        self.active: ctk.CTkFrame | None = None
        self.tagline: ctk.CTkLabel | None = None
        self.badge: ctk.CTkLabel | None = None
        self.title_row: ctk.CTkFrame | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.BuildHeader()
        self.BuildContent()

    def BuildHeader(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 8))
        header.grid_columnconfigure(0, weight=1)
        self.header = header

        accent = ctk.CTkFrame(header, height=3, fg_color=Theme.Accent, corner_radius=2)
        accent.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        accent.grid_propagate(False)

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.grid(row=1, column=0, sticky="ew")
        title_row.grid_columnconfigure(0, weight=1)
        title_row.grid_columnconfigure(1, weight=0)
        self.title_row = title_row

        self.title_widget = SectionTitle(title_row, "dice", "Dicer", icon_size=34, font=Fonts.Title())
        self.badge = Layout.Label(
            title_row,
            text=Locale.t("shell.client_badge"),
            font=Fonts.Caption(),
            text_color=Theme.Accent,
            fg_color=Theme.AccentMuted,
            corner_radius=6,
        )
        self.PlaceTitleRow()

        self.tagline = Layout.Label(
            header,
            text=Locale.t("shell.tagline"),
            font=Fonts.Subtitle(),
            text_color=Theme.TextMuted,
        )
        self.tagline.grid(row=2, column=0, sticky=Layout.Sticky(), pady=(8, 0))

    def PlaceTitleRow(self) -> None:
        if self.title_row is None:
            return

        self.title_widget.grid_forget()
        self.badge.grid_forget()

        if Layout.IsRtl():
            self.badge.grid(row=0, column=0, sticky=Layout.Sticky())
            self.title_widget.grid(row=0, column=1, sticky=Layout.Sticky())
        else:
            self.title_widget.grid(row=0, column=0, sticky=Layout.Sticky())
            self.badge.grid(row=0, column=1, sticky="e", padx=(12, 0))

    def BuildContent(self) -> None:
        self.card = ctk.CTkFrame(
            self,
            fg_color=Theme.Surface,
            corner_radius=Theme.Radius,
            border_width=1,
            border_color=Theme.Border,
        )
        self.card.grid(row=1, column=0, sticky="ew", padx=32, pady=(8, 28))
        self.card.grid_columnconfigure(0, weight=1)
        self.card.grid_rowconfigure(0, weight=0)

        self.stage = ctk.CTkFrame(self.card, fg_color="transparent")
        self.stage.grid(row=0, column=0, sticky="ew", padx=24, pady=24)
        self.stage.grid_columnconfigure(0, weight=1)

    def Refresh(self) -> None:
        if self.tagline is not None:
            self.tagline.configure(
                text=Locale.t("shell.tagline"),
                anchor=Layout.Anchor(),
                justify=Layout.Justify(),
            )

        if self.badge is not None:
            if Store.UserId and Store.Username:
                badge_text = Locale.t("shell.user_badge", username=Store.Username)
            else:
                badge_text = Locale.t("shell.client_badge")

            self.badge.configure(
                text=badge_text,
                anchor=Layout.Anchor(),
                justify=Layout.Justify(),
            )

        self.PlaceTitleRow()

    def ClearActive(self) -> None:
        self.active = None

    def Show(self, screen: ctk.CTkFrame) -> None:
        if self.active is not None and self.active is not screen:
            try:
                self.active.grid_forget()
            except Exception:
                pass

        self.active = screen
        screen.grid(row=0, column=0, sticky="ew")

        window = self.winfo_toplevel()
        if hasattr(window, "FitWindow"):
            window.after_idle(window.FitWindow)
