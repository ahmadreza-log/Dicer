import customtkinter as ctk

from Fonts import Fonts
from Icons import Icons
from i18n.Locale import Locale
from Layout import Layout
from Theme import Theme


class SectionTitle(ctk.CTkFrame):
    # Heading row with a local emoji icon and title text.

    def __init__(
        self,
        master,
        icon: str,
        title: str,
        icon_size: int = 26,
        font=None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        image = Icons.Get(icon, icon_size)
        icon_label = None

        if image is not None:
            icon_label = ctk.CTkLabel(self, text="", image=image)
            icon_label.image = image

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=font or Fonts.Heading(),
            text_color=Theme.Text,
            anchor=Layout.Anchor(),
            justify=Layout.Justify(),
        )

        if Layout.IsRtl():
            title_label.pack(side=Layout.PackStart())

            if icon_label is not None:
                icon_label.pack(side=Layout.PackStart(), padx=(10, 0))
        else:
            if icon_label is not None:
                icon_label.pack(side=Layout.PackStart(), padx=(0, 10))

            title_label.pack(side=Layout.PackStart())


class FormField(ctk.CTkFrame):
    # Label + input pair used on settings forms.

    def __init__(self, master, label: str, placeholder: str = "", show: str | None = None, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.grid_columnconfigure(0, weight=1)

        Layout.Label(
            self,
            text=label,
            font=Fonts.Caption(),
            text_color=Theme.TextMuted,
        ).grid(row=0, column=0, sticky=Layout.Sticky(), pady=(0, 6))

        entry_kwargs = {}

        if show is not None:
            entry_kwargs["show"] = show

        self.input = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            height=42,
            corner_radius=Theme.RadiusSmall,
            border_color=Theme.Border,
            fg_color=Theme.SurfaceRaised,
            font=Fonts.Body(),
            justify=Layout.Justify(),
            **entry_kwargs,
        )
        self.input.grid(row=1, column=0, sticky="ew")

    def Get(self) -> str:
        return self.input.get().strip()

    def Set(self, value: str) -> None:
        self.input.delete(0, "end")
        self.input.insert(0, value)


class MenuButton(ctk.CTkButton):
    # Styled menu row with a local icon image and variant-based colors.

    Height = 52
    IconSize = 24

    Styles = {
        "primary": {
            "fg_color": Theme.SurfaceRaised,
            "hover_color": Theme.AccentMuted,
            "border_color": Theme.Border,
            "text_color": Theme.Text,
        },
        "accent": {
            "fg_color": Theme.Accent,
            "hover_color": Theme.AccentHover,
            "border_color": Theme.Accent,
            "text_color": "#ffffff",
        },
        "danger": {
            "fg_color": Theme.SurfaceRaised,
            "hover_color": Theme.DangerMuted,
            "border_color": Theme.Border,
            "text_color": Theme.TextMuted,
        },
    }

    def __init__(
        self,
        master,
        icon: str,
        label: str,
        command,
        variant: str = "primary",
        **kwargs,
    ) -> None:
        style = self.Styles.get(variant, self.Styles["primary"])
        image = Icons.Get(icon, self.IconSize)
        text = f"{label}  " if Layout.IsRtl() else f"  {label}"

        super().__init__(
            master,
            text=text,
            command=command,
            height=self.Height,
            corner_radius=Theme.RadiusSmall,
            border_width=1,
            anchor=Layout.ButtonAnchor(),
            image=image,
            compound=Layout.Compound(),
            font=Fonts.ButtonBold() if variant == "accent" else Fonts.Button(),
            **style,
            **kwargs,
        )

        if image is not None:
            self._icon = image

        if variant == "danger":
            self.bind("<Enter>", self._OnEnterDanger)
            self.bind("<Leave>", self._OnLeaveDanger)

    def _OnEnterDanger(self, _event) -> None:
        self.configure(
            border_color=Theme.Danger,
            text_color=Theme.DangerHover,
        )

    def _OnLeaveDanger(self, _event) -> None:
        self.configure(
            border_color=Theme.Border,
            text_color=Theme.TextMuted,
        )


class BackButton(ctk.CTkButton):
    # Compact back control for nested screens.

    def __init__(self, master, command, **kwargs) -> None:
        super().__init__(
            master,
            text=Locale.t("common.back"),
            command=command,
            width=110 if Layout.IsRtl() else 96,
            height=34,
            corner_radius=8,
            fg_color=Theme.SurfaceRaised,
            hover_color=Theme.Border,
            border_width=1,
            border_color=Theme.Border,
            text_color=Theme.TextMuted,
            font=Fonts.Caption(),
            anchor=Layout.ButtonAnchor(),
            **kwargs,
        )


class RoleButton(ctk.CTkFrame):
    # Clickable role row with icon image and a bold highlighted phrase.

    Height = 56
    IconSize = 28

    def __init__(
        self,
        master,
        icon: str,
        prefix: str,
        highlight: str,
        command,
        **kwargs,
    ) -> None:
        super().__init__(
            master,
            height=self.Height,
            corner_radius=Theme.RadiusSmall,
            fg_color=Theme.SurfaceRaised,
            border_width=1,
            border_color=Theme.Border,
            **kwargs,
        )
        self.grid_propagate(False)
        self.command = command

        self.bind("<Enter>", self._OnEnter)
        self.bind("<Leave>", self._OnLeave)
        self.bind("<Button-1>", self._OnClick)

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="both", expand=True, padx=18, pady=12)
        row.bind("<Enter>", self._OnEnter)
        row.bind("<Leave>", self._OnLeave)
        row.bind("<Button-1>", self._OnClick)

        image = Icons.Get(icon, self.IconSize)
        icon_label = ctk.CTkLabel(row, text="", image=image, width=32)

        if image is not None:
            icon_label.image = image

        text = ctk.CTkFrame(row, fg_color="transparent")

        prefix_label = ctk.CTkLabel(
            text,
            text=prefix,
            font=Fonts.Button(),
            text_color=Theme.TextMuted,
            anchor=Layout.Anchor(),
        )
        highlight_label = ctk.CTkLabel(
            text,
            text=highlight,
            font=Fonts.ButtonBold(),
            text_color=Theme.Accent,
            anchor=Layout.Anchor(),
        )

        if Layout.IsRtl():
            text.pack(side=Layout.PackStart(), fill="x", expand=True, padx=(0, 8))
            icon_label.pack(side=Layout.PackStart())
            prefix_label.pack(side=Layout.PackStart())
            highlight_label.pack(side=Layout.PackStart())
        else:
            icon_label.pack(side=Layout.PackStart())
            text.pack(side=Layout.PackStart(), fill="x", expand=True, padx=(8, 0))
            prefix_label.pack(side=Layout.PackStart())
            highlight_label.pack(side=Layout.PackStart())

        icon_label.bind("<Button-1>", self._OnClick)
        text.bind("<Button-1>", self._OnClick)
        prefix_label.bind("<Button-1>", self._OnClick)
        highlight_label.bind("<Button-1>", self._OnClick)

        widgets = (self, row, icon_label, text, prefix_label, highlight_label)
        for widget in widgets:
            widget.configure(cursor="hand2")

    def _OnEnter(self, _event) -> None:
        self.configure(fg_color=Theme.AccentMuted, border_color=Theme.Accent)

    def _OnLeave(self, _event) -> None:
        self.configure(fg_color=Theme.SurfaceRaised, border_color=Theme.Border)

    def _OnClick(self, _event) -> None:
        self.command()
