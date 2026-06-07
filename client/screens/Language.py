import customtkinter as ctk

from Fonts import Fonts
from i18n.Locale import Locale
from Layout import Layout
from Store import Store
from Theme import Theme
from Widgets import BackButton, FormField, MenuButton, SectionTitle


class Language(ctk.CTkFrame):
    # Language selection screen.

    def __init__(self, master, navigator, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.navigator = navigator
        self.labels = {label: code for code, label in Locale.Choices()}

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

        SectionTitle(titles, "bolt", Locale.t("language.title")).grid(row=0, column=0, sticky=Layout.Sticky())

        Layout.Label(
            titles,
            text=Locale.t("language.subtitle"),
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

        Layout.Label(
            form,
            text=Locale.t("language.label"),
            font=Fonts.Caption(),
            text_color=Theme.TextMuted,
        ).grid(row=0, column=0, sticky=Layout.Sticky(), pady=(0, 6))

        self.selector = ctk.CTkOptionMenu(
            form,
            values=[label for label in self.labels],
            height=42,
            corner_radius=Theme.RadiusSmall,
            fg_color=Theme.SurfaceRaised,
            button_color=Theme.Accent,
            button_hover_color=Theme.AccentHover,
            dropdown_fg_color=Theme.SurfaceRaised,
            font=Fonts.Body(),
        )
        self.selector.grid(row=1, column=0, sticky="ew", pady=(0, 16))

        MenuButton(
            form,
            icon="play",
            label=Locale.t("language.save"),
            command=self.OnSave,
            variant="accent",
        ).grid(row=2, column=0, sticky="ew")

        self.LoadFields()

    def LoadFields(self) -> None:
        current_label = dict(Locale.Choices()).get(Locale.Code, "English")
        self.selector.set(current_label)

    def OnBack(self) -> None:
        self.navigator.ShowSettings()

    def OnSave(self) -> None:
        code = self.labels.get(self.selector.get(), Locale.DefaultCode)
        Locale.Set(code)
        Store.SaveLocale(code)

        if self.navigator.on_locale_change:
            self.navigator.on_locale_change()

        label = dict(Locale.Choices()).get(code, code)
        self.navigator.ShowNotice(
            Locale.t("language.saved.title"),
            Locale.t("language.saved.body", language=label),
            success=True,
        )
