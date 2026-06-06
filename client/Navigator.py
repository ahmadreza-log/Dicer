from screens.MainMenu import MainMenu
from screens.Network import Network
from screens.Notice import Notice
from screens.SettingsMenu import SettingsMenu
from screens.Start import Start


class Navigator:
    # Routes between client screens inside the shared shell container.

    def __init__(self, shell) -> None:
        self.shell = shell
        self.menu = MainMenu(shell.stage, self)
        self.start = Start(shell.stage, self)
        self.settings = SettingsMenu(shell.stage, self)
        self.network = Network(shell.stage, self)
        self.notice: Notice | None = None
        self.ShowMenu()

    def ShowMenu(self) -> None:
        self.shell.Show(self.menu)

    def ShowStart(self) -> None:
        self.shell.Show(self.start)

    def ShowSettings(self) -> None:
        self.shell.Show(self.settings)

    def ShowNetwork(self) -> None:
        self.network.LoadFields()
        self.shell.Show(self.network)

    def ShowNotice(self, title: str, message: str, success: bool = True) -> None:
        self.notice = Notice(
            self.shell.stage,
            self,
            title=title,
            message=message,
            success=success,
        )
        self.shell.Show(self.notice)
