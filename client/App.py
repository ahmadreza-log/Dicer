import customtkinter as ctk

from Navigator import Navigator
from network.Session import Session
from screens.Shell import Shell
from Theme import Theme


class App(ctk.CTk):
    # Root CustomTkinter window for the Dicer client.

    Title = "Dicer Client"

    def __init__(self) -> None:
        Theme.Apply()
        super().__init__()

        self.title(self.Title)
        self.geometry(f"{Theme.Width}x{Theme.Height}")
        self.minsize(Theme.MinWidth, Theme.MinHeight)
        self.configure(fg_color=Theme.Background)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.shell = Shell(self, self)
        self.shell.grid(row=0, column=0, sticky="nsew")

        self.navigator = Navigator(self.shell)
        self.protocol("WM_DELETE_WINDOW", self.OnClose)

    def OnClose(self) -> None:
        Session.Disconnect()
        self.destroy()

    def Run(self) -> None:
        self.mainloop()
