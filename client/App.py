import customtkinter as ctk

from screens.MainMenu import MainMenu
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

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu = MainMenu(self)
        self.menu.grid(row=0, column=0, sticky="nsew")

    def Run(self) -> None:
        self.mainloop()
