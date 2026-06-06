import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate

from board.Bridge import Bridge
from board.Forms import Forms
from board.Service import Service
from board.Settings import Settings as Panel
from board.Shell import Shell
from cli.Panel import Panel as CliPanel
from database.Settings import Settings as Database


class Callbacks:
    # Registers all Dash callbacks for the management dashboard.

    @classmethod
    def Register(cls, application) -> None:
        cls.RegisterNavigation(application)
        cls.RegisterRefresh(application)
        cls.RegisterControls(application)
        cls.RegisterFormLoads(application)
        cls.RegisterSettings(application)
        cls.RegisterStorage(application)

    @classmethod
    def RegisterNavigation(cls, application) -> None:
        pages = Shell.Pages

        @application.callback(
            Output("page", "data"),
            Output("topbar-title", "children"),
            Output("topbar-subtitle", "children"),
            *[Output(f"nav-{page}", "className") for page in pages],
            *[Output(f"page-{page}", "style") for page in pages],
            [Input(f"nav-{page}", "n_clicks") for page in pages],
            State("page", "data"),
            prevent_initial_call=True,
        )
        def Navigate(*args):
            current = args[-1]
            triggered = cls.Trigger()

            if not triggered or not triggered.startswith("nav-"):
                raise PreventUpdate

            page = triggered.replace("nav-", "")
            title = Shell.Titles.get(page, "Dicer")
            subtitle = Shell.Subtitles.get(page, "")

            nav_classes = [
                "sidebar-link active" if item == page else "sidebar-link"
                for item in pages
            ]

            page_styles = [
                {"display": "block"} if item == page else {"display": "none"}
                for item in pages
            ]

            return page, title, subtitle, *nav_classes, *page_styles

    @classmethod
    def RegisterRefresh(cls, application) -> None:
        @application.callback(
            Output("metric-state", "children"),
            Output("metric-host", "children"),
            Output("metric-uptime", "children"),
            Output("metric-clients", "children"),
            Output("client-chart", "figure"),
            Output("client-table", "children"),
            Output("dash-db-summary", "children"),
            Output("activity-feed", "children"),
            Output("topbar-status", "children"),
            Output("topbar-status", "className"),
            Output("topbar-clock", "children"),
            Output("alert-banner", "children"),
            Output("clients-full-table", "children"),
            Output("clients-count", "children"),
            Output("settings-overview", "children"),
            Input("refresh", "n_intervals"),
        )
        def Refresh(interval):
            Bridge.Record()
            status = Bridge.Status()
            database = Bridge.Database()
            clients = Bridge.Clients()

            state = "Running" if status["active"] else "Stopped"
            host = f"{status['host']}:{status['port']}"
            uptime = CliPanel.FormatUptime(status["uptime"])
            count = str(status["clients"])

            figure = cls.BuildChart()
            table = cls.BuildTable(clients)
            dbinfo = cls.BuildDatabaseSummary(database)
            activity = cls.BuildActivity()
            pill_class = "status-pill running" if status["active"] else "status-pill stopped"
            pill = [
                html.Span(className="pulse-dot") if status["active"] else "●",
                f" {state}",
            ]
            clock = cls.BuildClock()
            alert = cls.BuildAlert(Bridge.alert)
            full_table = cls.BuildFullTable(clients)
            count_text = f"{len(clients)} active connection(s)"
            overview = cls.BuildOverview()

            return (
                state,
                host,
                uptime,
                count,
                figure,
                table,
                dbinfo,
                activity,
                pill,
                pill_class,
                clock,
                alert,
                full_table,
                count_text,
                overview,
            )

    @classmethod
    def RegisterControls(cls, application) -> None:
        @application.callback(
            Output("control-message", "children"),
            Input("btn-start", "n_clicks"),
            Input("btn-stop", "n_clicks"),
            Input("btn-restart", "n_clicks"),
            prevent_initial_call=True,
        )
        def Control(start, stop, restart):
            trigger = cls.Trigger()

            if trigger == "btn-start":
                success, message = Bridge.manager.Start()
            elif trigger == "btn-stop":
                success, message = Bridge.manager.Stop()
            elif trigger == "btn-restart":
                success, message = Bridge.manager.Restart()
            else:
                raise PreventUpdate

            kind = "success" if success else "warning"
            Bridge.Log(message, kind)
            prefix = "✅" if success else "⚠️"
            return f"{prefix} {message}"

    @classmethod
    def RegisterFormLoads(cls, application) -> None:
        @application.callback(
            Output("set-net-mode", "value"),
            Output("set-net-host", "value"),
            Output("set-net-port", "value"),
            Output("set-net-max", "value"),
            Output("set-net-auto", "value"),
            Input("page", "data"),
        )
        def LoadNetwork(page):
            if page != "network":
                raise PreventUpdate

            values = Forms.Values()["net"]
            return (
                values["mode"],
                values["host"],
                values["port"],
                values["max"],
                values["auto"],
            )

        @application.callback(
            Output("set-log-enabled", "value"),
            Output("set-log-level", "value"),
            Output("set-log-console", "value"),
            Output("set-log-file", "value"),
            Output("set-log-dir", "value"),
            Output("set-log-name", "value"),
            Output("set-log-size", "value"),
            Output("set-log-backups", "value"),
            Input("page", "data"),
        )
        def LoadLogging(page):
            if page != "logging":
                raise PreventUpdate

            values = Forms.Values()["log"]
            return (
                values["enabled"],
                values["level"],
                values["console"],
                values["file"],
                values["dir"],
                values["name"],
                values["size"],
                values["backups"],
            )

        @application.callback(
            Output("set-con-welcome", "value"),
            Output("set-con-buffer", "value"),
            Output("set-con-timeout", "value"),
            Output("set-con-max", "value"),
            Input("page", "data"),
        )
        def LoadConnection(page):
            if page != "connection":
                raise PreventUpdate

            values = Forms.Values()["con"]
            return values["welcome"], values["buffer"], values["timeout"], values["max"]

        @application.callback(
            Output("set-sec-pass", "value"),
            Output("set-sec-allowed", "value"),
            Output("set-sec-blocked", "value"),
            Input("page", "data"),
        )
        def LoadSecurity(page):
            if page != "security":
                raise PreventUpdate

            values = Forms.Values()["sec"]
            return values["pass"], values["allowed"], values["blocked"]

        @application.callback(
            Output("set-db-enabled", "value"),
            Output("set-db-host", "value"),
            Output("set-db-port", "value"),
            Output("set-db-user", "value"),
            Output("set-db-pass", "value"),
            Output("set-db-name", "value"),
            Input("page", "data"),
        )
        def LoadDatabase(page):
            if page != "database":
                raise PreventUpdate

            values = Forms.Values()["db"]
            return (
                values["enabled"],
                values["host"],
                values["port"],
                values["user"],
                values["pass"],
                values["name"],
            )

        @application.callback(
            Output("set-panel-host", "value"),
            Output("set-panel-port", "value"),
            Output("set-panel-interval", "value"),
            Output("set-panel-debug", "value"),
            Input("page", "data"),
        )
        def LoadPanel(page):
            if page != "panel":
                raise PreventUpdate

            values = Forms.Values()["panel"]
            return values["host"], values["port"], values["interval"], values["debug"]

    @classmethod
    def RegisterSettings(cls, application) -> None:
        cls.RegisterPanelSync(application)
        @application.callback(
            Output("set-net-message", "children"),
            Input("btn-net-apply", "n_clicks"),
            State("set-net-mode", "value"),
            State("set-net-host", "value"),
            State("set-net-port", "value"),
            State("set-net-max", "value"),
            State("set-net-auto", "value"),
            prevent_initial_call=True,
        )
        def ApplyNetwork(clicks, mode, host, port, max_clients, auto):
            auto_start = "yes" in (auto or [])
            success, message = Service.ApplyNetwork(
                Bridge.manager,
                host or "",
                str(port or ""),
                mode or "Local",
                str(max_clients if max_clients is not None else 0),
                auto_start,
            )
            kind = "success" if success else "warning"
            Bridge.Log(message, kind)
            return cls.Message(message, success)

        @application.callback(
            Output("set-log-message", "children"),
            Input("btn-log-apply", "n_clicks"),
            State("set-log-enabled", "value"),
            State("set-log-level", "value"),
            State("set-log-console", "value"),
            State("set-log-file", "value"),
            State("set-log-dir", "value"),
            State("set-log-name", "value"),
            State("set-log-size", "value"),
            State("set-log-backups", "value"),
            prevent_initial_call=True,
        )
        def ApplyLogging(clicks, enabled, level, console, file, directory, filename, size, backups):
            success, message = Service.ApplyLogging(
                "yes" in (enabled or []),
                level or "INFO",
                "yes" in (console or []),
                "yes" in (file or []),
                directory or "",
                filename or "",
                str(size or 1),
                str(backups if backups is not None else 0),
            )
            kind = "success" if success else "warning"
            Bridge.Log(message, kind)
            return cls.Message(message, success)

        @application.callback(
            Output("set-con-message", "children"),
            Input("btn-con-apply", "n_clicks"),
            State("set-con-welcome", "value"),
            State("set-con-buffer", "value"),
            State("set-con-timeout", "value"),
            State("set-con-max", "value"),
            prevent_initial_call=True,
        )
        def ApplyConnection(clicks, welcome, buffer, timeout, max_per):
            success, message = Service.ApplyConnection(
                Bridge.manager,
                welcome or "",
                str(buffer or 0),
                str(timeout if timeout is not None else 0),
                str(max_per if max_per is not None else 0),
            )
            kind = "success" if success else "warning"
            Bridge.Log(message, kind)
            return cls.Message(message, success)

        @application.callback(
            Output("set-sec-message", "children"),
            Input("btn-sec-apply", "n_clicks"),
            State("set-sec-pass", "value"),
            State("set-sec-allowed", "value"),
            State("set-sec-blocked", "value"),
            prevent_initial_call=True,
        )
        def ApplySecurity(clicks, password, allowed, blocked):
            success, message = Service.ApplySecurity(
                password or "",
                allowed or "",
                blocked or "",
            )
            kind = "success" if success else "warning"
            Bridge.Log(message, kind)
            return cls.Message(message, success)

        @application.callback(
            Output("set-db-message", "children"),
            Input("btn-db-apply", "n_clicks"),
            Input("btn-db-test", "n_clicks"),
            Input("btn-db-connect", "n_clicks"),
            Input("btn-db-disconnect", "n_clicks"),
            State("set-db-enabled", "value"),
            State("set-db-host", "value"),
            State("set-db-port", "value"),
            State("set-db-user", "value"),
            State("set-db-pass", "value"),
            State("set-db-name", "value"),
            prevent_initial_call=True,
        )
        def DatabaseAction(apply, test, connect, disconnect, enabled, host, port, user, password, name):
            trigger = cls.Trigger()

            if trigger == "btn-db-test":
                success, message = Service.TestDatabase()
            elif trigger == "btn-db-connect":
                success, message = Service.ConnectDatabase()
            elif trigger == "btn-db-disconnect":
                success, message = Service.DisconnectDatabase()
            elif trigger == "btn-db-apply":
                success, message = Service.ApplyDatabase(
                    Bridge.manager,
                    "yes" in (enabled or []),
                    host or "",
                    str(port or ""),
                    user or "",
                    password or "",
                    name or "",
                )
            else:
                raise PreventUpdate

            kind = "success" if success else "warning"
            Bridge.Log(message, kind)
            return cls.Message(message, success)

        @application.callback(
            Output("set-panel-message", "children"),
            Output("refresh", "interval", allow_duplicate=True),
            Input("btn-panel-apply", "n_clicks"),
            State("set-panel-host", "value"),
            State("set-panel-port", "value"),
            State("set-panel-interval", "value"),
            State("set-panel-debug", "value"),
            prevent_initial_call=True,
        )
        def ApplyPanel(clicks, host, port, interval, debug):
            success, message, refresh = Service.ApplyPanel(
                host or "",
                str(port or ""),
                str(interval or ""),
                "yes" in (debug or []),
            )
            kind = "success" if success else "warning"
            Bridge.Log(message, kind)
            return cls.Message(message, success), refresh

    @classmethod
    def RegisterPanelSync(cls, application) -> None:
        @application.callback(
            Output("refresh", "interval", allow_duplicate=True),
            Input("page", "data"),
            prevent_initial_call="initial_duplicate",
        )
        def SyncRefreshInterval(page):
            from board.Settings import Settings as PanelSettings

            return PanelSettings.Interval

    @classmethod
    def RegisterStorage(cls, application) -> None:
        @application.callback(
            Output("set-store-message", "children"),
            Input("btn-store-save", "n_clicks"),
            prevent_initial_call=True,
        )
        def StorageSave(save):
            success, message = Service.Save()
            kind = "success" if success else "warning"
            Bridge.Log(message, kind)
            return cls.Message(message, success)

        @application.callback(
            Output("set-store-message", "children", allow_duplicate=True),
            Output("refresh", "interval", allow_duplicate=True),
            Input("btn-store-load", "n_clicks"),
            Input("btn-store-reset", "n_clicks"),
            prevent_initial_call=True,
        )
        def StorageReload(load, reset):
            from dash import no_update
            from board.Settings import Settings as PanelSettings

            trigger = cls.Trigger()

            if trigger == "btn-store-load":
                success, message = Service.Load(Bridge.manager)
            elif trigger == "btn-store-reset":
                success, message = Service.Reset(Bridge.manager)
            else:
                raise PreventUpdate

            kind = "success" if success else "warning"
            Bridge.Log(message, kind)
            interval = PanelSettings.Interval if success else no_update
            return cls.Message(message, success), interval

    @staticmethod
    def Trigger() -> str:
        from dash import ctx

        if not ctx.triggered:
            return ""

        return ctx.triggered_id or ""

    @classmethod
    def Message(cls, text: str, success: bool):
        color = "success" if success else "warning"
        prefix = "✅" if success else "⚠️"
        return dbc.Alert(f"{prefix} {text}", color=color, className="mb-0")

    @classmethod
    def BuildChart(cls):
        figure = go.Figure()
        times = [point["time"] for point in Bridge.history]
        counts = [point["clients"] for point in Bridge.history]

        figure.add_trace(
            go.Scatter(
                x=times,
                y=counts,
                mode="lines+markers",
                fill="tozeroy",
                line={"color": "#00bc8c", "width": 2, "shape": "spline"},
                marker={"size": 5, "color": "#00bc8c"},
                name="Clients",
            )
        )

        figure.update_layout(
            template="plotly_dark",
            margin={"l": 40, "r": 20, "t": 20, "b": 40},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis={"title": "Time", "showgrid": True, "gridcolor": "rgba(255,255,255,0.06)"},
            yaxis={"title": "Clients", "rangemode": "tozero", "gridcolor": "rgba(255,255,255,0.06)"},
            height=320,
            hovermode="x unified",
        )

        return figure

    @classmethod
    def BuildTable(cls, clients: list[str]):
        if not clients:
            return dbc.Alert("No clients connected.", color="secondary", className="mb-0")

        rows = [html.Tr([html.Th("#"), html.Th("Address")])]

        for index, address in enumerate(clients[:8], start=1):
            rows.append(html.Tr([html.Td(str(index)), html.Td(address)]))

        if len(clients) > 8:
            rows.append(html.Tr([html.Td("…"), html.Td(f"+{len(clients) - 8} more")]))

        return dbc.Table(
            [html.Thead(rows[0]), html.Tbody(rows[1:])],
            bordered=True,
            hover=True,
            responsive=True,
            className="mb-0",
        )

    @classmethod
    def BuildFullTable(cls, clients: list[str]):
        if not clients:
            return dbc.Alert("No clients connected.", color="secondary", className="mb-0")

        rows = [html.Tr([html.Th("#"), html.Th("Address"), html.Th("Status")])]

        for index, address in enumerate(clients, start=1):
            rows.append(
                html.Tr([
                    html.Td(str(index)),
                    html.Td(address),
                    html.Td(dbc.Badge("Active", color="success")),
                ])
            )

        return dbc.Table(
            [html.Thead(rows[0]), html.Tbody(rows[1:])],
            bordered=True,
            hover=True,
            striped=True,
            responsive=True,
            className="mb-0",
        )

    @classmethod
    def BuildDatabaseSummary(cls, database: dict):
        active = database["active"]
        badge = dbc.Badge("Connected", color="success") if active else dbc.Badge("Offline", color="secondary")

        return html.Div(
            [
                html.Div([html.Strong("MySQL "), badge], className="mb-2"),
                html.P(f"{database['host']}:{database['port']}", className="mb-1 small"),
                html.P(f"Schema: {database['name']}", className="mb-0 small text-muted"),
            ]
        )

    @classmethod
    def BuildActivity(cls):
        if not Bridge.activities:
            return html.P("No recent activity.", className="text-muted small mb-0")

        items = []

        for entry in Bridge.activities[:8]:
            items.append(
                html.Div(
                    className="activity-item",
                    children=[
                        html.Div(entry["message"]),
                        html.Div(entry["time"], className="activity-time"),
                    ],
                )
            )

        return html.Div(items)

    @classmethod
    def BuildClock(cls):
        from datetime import datetime

        return datetime.now().strftime("%H:%M:%S")

    @classmethod
    def BuildOverview(cls):
        from board.Overview import Overview

        return Overview.Build(Bridge.manager)

    @classmethod
    def BuildAlert(cls, message: str):
        if not message:
            return ""

        color = "success" if message.startswith("✅") or "started" in message.lower() else "info"

        if "fail" in message.lower() or "error" in message.lower() or "⚠️" in message:
            color = "warning"

        return dbc.Alert(message, color=color, className="mb-0")
