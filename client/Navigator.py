from screens.Account import Account
from screens.Auth import Auth
from screens.JoinRoom import JoinRoom
from screens.Language import Language
from screens.MainMenu import MainMenu
from screens.Network import Network
from screens.Notice import Notice
from screens.Register import Register
from screens.Room import Room
from screens.SettingsMenu import SettingsMenu
from screens.Start import Start
from screens.VerifyEmail import VerifyEmail


from Store import Store
from network.Session import Session


class Navigator:
    # Routes between client screens inside the shared shell container.

    def __init__(self, shell, on_locale_change=None) -> None:
        self.shell = shell
        self.on_locale_change = on_locale_change
        self.current = "auth"
        self.join_role = "adventure"
        self.notice: Notice | None = None
        self.BuildScreens()
        self.ShowInitialScreen()

    def IsAuthenticated(self) -> bool:
        return Store.UserId > 0 and Store.Active

    def ShowInitialScreen(self) -> None:
        if self.IsAuthenticated():
            self.ShowMenu()
        elif Store.UserId:
            self.ShowVerifyEmail()
        else:
            self.ShowAuth()

    def BuildScreens(self) -> None:
        self.menu = MainMenu(self.shell.stage, self)
        self.start = Start(self.shell.stage, self)
        self.join = JoinRoom(self.shell.stage, self)
        self.settings = SettingsMenu(self.shell.stage, self)
        self.language = Language(self.shell.stage, self)
        self.network = Network(self.shell.stage, self)
        self.room = Room(self.shell.stage, self)
        self.account = Account(self.shell.stage, self)
        self.auth = Auth(self.shell.stage, self)
        self.register = Register(self.shell.stage, self)
        self.verify = VerifyEmail(self.shell.stage, self)

    def ReloadScreens(self) -> None:
        current = self.current

        self.shell.ClearActive()

        for screen in (
            self.menu,
            self.start,
            self.join,
            self.settings,
            self.language,
            self.network,
            self.room,
            self.account,
            self.auth,
            self.register,
            self.verify,
        ):
            screen.destroy()

        if self.notice is not None:
            self.notice.destroy()
            self.notice = None

        self.BuildScreens()

        routes = {
            "menu": self.ShowMenu,
            "start": self.ShowStart,
            "join": lambda: self.ShowJoinRoom(self.join_role),
            "settings": self.ShowSettings,
            "language": self.ShowLanguage,
            "network": self.ShowNetwork,
            "room": self.ShowRoom,
            "account": self.ShowAccount,
            "auth": self.ShowAuth,
            "register": self.ShowRegister,
            "verify": self.ShowVerifyEmail,
        }
        routes.get(current, self.ShowInitialScreen)()

    def ShowMenu(self) -> None:
        self.current = "menu"
        Session.EnsurePresence()
        self.shell.Show(self.menu)

    def ShowStart(self) -> None:
        self.current = "start"
        self.shell.Show(self.start)

    def ShowJoinRoom(self, role: str) -> None:
        self.current = "join"
        self.join_role = role
        self.join.Prepare(role)
        self.shell.Show(self.join)

    def ShowSettings(self) -> None:
        self.current = "settings"
        self.shell.Show(self.settings)

    def ShowLanguage(self) -> None:
        self.current = "language"
        self.language.LoadFields()
        self.shell.Show(self.language)

    def ShowNetwork(self) -> None:
        self.current = "network"
        self.network.LoadFields()
        self.shell.Show(self.network)

    def ShowRoom(self) -> None:
        self.current = "room"
        self.room.Refresh()
        self.shell.Show(self.room)

    def ShowAuth(self) -> None:
        self.current = "auth"
        self.shell.Show(self.auth)

    def ShowAccount(self) -> None:
        self.current = "account"
        self.account.Refresh()
        self.shell.Show(self.account)

    def ShowRegister(self) -> None:
        self.current = "register"
        self.shell.Show(self.register)

    def ShowVerifyEmail(self) -> None:
        self.current = "verify"
        self.verify.Refresh()
        self.shell.Show(self.verify)

    def ShowNotice(self, title: str, message: str, success: bool = True) -> None:
        self.notice = Notice(
            self.shell.stage,
            self,
            title=title,
            message=message,
            success=success,
        )
        self.shell.Show(self.notice)
