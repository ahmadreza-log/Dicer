import customtkinter as ctk

from i18n.Locale import Locale
from Navigator import Navigator
from network.Session import Session
from screens.Shell import Shell
from Theme import Theme


class App(ctk.CTk):
    # Root CustomTkinter window for the Dicer client.

    def __init__(self) -> None:
        Theme.Apply()
        super().__init__()

        self.title(Locale.t("app.title"))
        self.geometry(f"{Theme.Width}x{Theme.MinHeight}")
        self.minsize(Theme.MinWidth, Theme.MinHeight)
        self.configure(fg_color=Theme.Background)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)

        self.shell = Shell(self, self)
        self.shell.grid(row=0, column=0, sticky="new")

        self.navigator = Navigator(self.shell, on_locale_change=self.RefreshLocale)
        self.protocol("WM_DELETE_WINDOW", self.OnClose)
        self.after_idle(self.FitWindow)

    def FitWindow(self) -> None:
        width = max(Theme.MinWidth, Theme.Width)
        self.geometry(f"{width}x{Theme.MinHeight}")
        self.update_idletasks()

        content_width = self.shell.winfo_reqwidth()
        content_height = self.shell.winfo_reqheight()

        width = max(content_width, Theme.MinWidth, Theme.Width)
        height = max(content_height, Theme.MinHeight)

        screen_height = self.winfo_screenheight()
        max_height = int(screen_height * Theme.MaxHeightRatio)
        height = min(height, max_height)

        self.geometry(f"{width}x{height}")
        self.minsize(Theme.MinWidth, Theme.MinHeight)

    def RefreshLocale(self) -> None:
        self.title(Locale.t("app.title"))
        self.shell.Refresh()
        self.navigator.ReloadScreens()
        self.after_idle(self.FitWindow)

    def OnClose(self) -> None:
        Session.Disconnect()
        self.destroy()

    def Run(self) -> None:
        self.mainloop()
