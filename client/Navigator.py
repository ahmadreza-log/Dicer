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


from i18n.Locale import Locale
from Store import Store
from network.Session import Session


class Navigator:
    # Routes between client screens inside the shared shell container.

    def __init__(self, shell, on_locale_change=None) -> None:
        self.shell = shell
        self.on_locale_change = on_locale_change
        self.current = "auth"
        self.join_role = "adventure"
        self.history: list[str] = []
        self._skip_history = False
        self.notice_return: str | None = None
        self.notice: Notice | None = None
        self.BuildScreens()
        Session.SetRoomClosedHandler(self.OnRoomClosed)
        self.ShowInitialScreen()

    def IsAuthenticated(self) -> bool:
        return Store.UserId > 0 and Store.Active

    def ShowInitialScreen(self) -> None:
        self.ResetTo("menu" if self.IsAuthenticated() else ("verify" if Store.UserId else "auth"))

    def ResetTo(self, screen: str) -> None:
        self.history.clear()
        self._skip_history = True

        try:
            self._GoTo(screen)
        finally:
            self._skip_history = False

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
        saved_history = list(self.history)

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
        self.history = saved_history
        self._skip_history = True

        try:
            self._GoTo(current)
        finally:
            self._skip_history = False

    def _PushHistory(self) -> None:
        if self._skip_history or not self.current:
            return

        self.history.append(self.current)

    def _GoTo(self, screen: str) -> None:
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
        route = routes.get(screen, self.ShowInitialScreen)
        route()

    def GoBack(self) -> None:
        if not self.history:
            self._skip_history = True

            try:
                if self.IsAuthenticated():
                    self.ShowMenu()
                else:
                    self.ShowInitialScreen()
            finally:
                self._skip_history = False
            return

        target = self.history.pop()
        self._skip_history = True

        try:
            self._GoTo(target)
        finally:
            self._skip_history = False

    def ReturnFromNotice(self) -> None:
        target = self.notice_return or self.current
        self.notice_return = None
        self._skip_history = True

        try:
            self._GoTo(target)
        finally:
            self._skip_history = False

    def ShowMenu(self) -> None:
        self._PushHistory()
        self.current = "menu"
        Session.EnsurePresence()
        self.shell.Refresh()
        self.shell.Show(self.menu)

    def ShowStart(self) -> None:
        self._PushHistory()
        self.current = "start"
        self.shell.Show(self.start)

    def ShowJoinRoom(self, role: str) -> None:
        self._PushHistory()
        self.current = "join"
        self.join_role = role
        self.join.Prepare(role)
        self.shell.Show(self.join)

    def ShowSettings(self) -> None:
        self._PushHistory()
        self.current = "settings"
        self.shell.Show(self.settings)

    def ShowLanguage(self) -> None:
        self._PushHistory()
        self.current = "language"
        self.language.LoadFields()
        self.shell.Show(self.language)

    def ShowNetwork(self) -> None:
        self._PushHistory()
        self.current = "network"
        self.network.LoadFields()
        self.shell.Show(self.network)

    def ShowRoom(self) -> None:
        self._PushHistory()
        self.current = "room"
        self.room.Refresh()
        if hasattr(self.room, "leave_button"):
            self.room.leave_button.configure(state="normal")
        if hasattr(self.room, "back_button"):
            self.room.back_button.configure(state="normal")
        self.shell.Show(self.room)

    def ShowAuth(self) -> None:
        self._PushHistory()
        self.current = "auth"
        self.shell.Refresh()
        self.shell.Show(self.auth)

    def ShowAccount(self) -> None:
        self._PushHistory()
        self.current = "account"
        self.account.Refresh()
        self.shell.Show(self.account)

    def ShowRegister(self) -> None:
        self._PushHistory()
        self.current = "register"
        self.shell.Show(self.register)

    def ShowVerifyEmail(self) -> None:
        self._PushHistory()
        self.current = "verify"
        self.verify.Refresh()
        self.shell.Show(self.verify)

    def Logout(self) -> None:
        Session.Disconnect()
        Store.ClearUser()
        self.shell.Refresh()
        self.ResetTo("auth")

    def OnRoomClosed(self, reason: str = "") -> None:
        Session.Disconnect()

        message = reason.strip() or Locale.t("room.closed.body")

        def show() -> None:
            self.ShowNotice(
                Locale.t("room.closed.title"),
                message,
                success=False,
                return_to="menu",
            )

        self.shell.after(0, show)

    def ShowNotice(
        self,
        title: str,
        message: str,
        success: bool = True,
        return_to: str | None = None,
    ) -> None:
        self.notice_return = return_to
        self.notice = Notice(
            self.shell.stage,
            self,
            title=title,
            message=message,
            success=success,
        )
        self.shell.Show(self.notice)
