import atexit

import dash_bootstrap_components as dbc
from dash import Dash

from board.Bridge import Bridge
from board.Callbacks import Callbacks
from board.Layout import Layout
from board.Settings import Settings
from cli.Manager import Manager
from config.Settings import Settings as Network
from database.Engine import Engine
from database.Settings import Settings as Database


class App:
    # Plotly Dash 4.x web dashboard for Dicer server management.

    @classmethod
    def Create(cls) -> Dash:
        application = Dash(
            __name__,
            external_stylesheets=[dbc.themes.CYBORG, dbc.icons.BOOTSTRAP],
            suppress_callback_exceptions=True,
            title="Dicer Server Dashboard",
        )

        application.layout = Layout.Build()
        Callbacks.Register(application)

        return application

    @classmethod
    def Bootstrap(cls, manager: Manager) -> None:
        Bridge.Attach(manager)

        if Database.Enabled:
            success, message = Engine.EnsureConnected()

            if success:
                Bridge.Log(f"Database connected. {message}", "success")
            else:
                Bridge.Notify(f"Database unavailable: {message}")

        if Network.AutoStart and not manager.IsActive():
            manager.Start()

        atexit.register(Bridge.Cleanup)

    @classmethod
    def Run(
        cls,
        manager: Manager,
        host: str | None = None,
        port: int | None = None,
    ) -> None:
        cls.Bootstrap(manager)
        application = cls.Create()

        application.run(
            host=host or Settings.Host,
            port=port or Settings.Port,
            debug=Settings.Debug,
        )
