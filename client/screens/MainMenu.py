import customtkinter as ctk

from Theme import Theme


class MainMenu(ctk.CTkFrame):
    # Home screen with a dedicated area for primary action buttons.

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.BuildHeader()
        self.BuildBody()

    def BuildHeader(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 12))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="🎲 Dicer",
            font=ctk.CTkFont(size=32, weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text="Client Application",
            font=ctk.CTkFont(size=14),
            text_color="gray70",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

    def BuildBody(self) -> None:
        body = ctk.CTkFrame(self, corner_radius=16)
        body.grid(row=1, column=0, sticky="nsew", padx=32, pady=(12, 28))
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            body,
            text="Main Menu",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            body,
            text="Choose an action below.",
            font=ctk.CTkFont(size=13),
            text_color="gray70",
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(52, 0))

        self.buttons = ctk.CTkFrame(body, fg_color="transparent")
        self.buttons.grid(row=1, column=0, sticky="nsew", padx=24, pady=24)
        self.buttons.grid_columnconfigure(0, weight=1)

        self.BuildButtons()

    def BuildButtons(self) -> None:
        # Placeholder layout — add real actions here in next steps.
        ctk.CTkLabel(
            self.buttons,
            text="Buttons will be added here.",
            font=ctk.CTkFont(size=13),
            text_color="gray60",
        ).grid(row=0, column=0, sticky="nw")

    def AddButton(self, text: str, command, row: int) -> ctk.CTkButton:
        # Helper for adding menu buttons in a consistent style.
        button = ctk.CTkButton(
            self.buttons,
            text=text,
            command=command,
            height=44,
            corner_radius=10,
            fg_color=Theme.Accent,
            hover_color="#009f77",
            anchor="w",
        )
        button.grid(row=row, column=0, sticky="ew", pady=6)
        return button
