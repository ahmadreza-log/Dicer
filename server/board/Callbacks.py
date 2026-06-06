import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Input, Output, html

from board.Bridge import Bridge
from cli.Panel import Panel
from database.Engine import Engine
from database.Settings import Settings as Database


class Callbacks:
    # Registers all Dash callbacks for the management dashboard.

    @classmethod
    def Register(cls, application) -> None:
        cls.RegisterRefresh(application)
        cls.RegisterControls(application)
        cls.RegisterDatabase(application)

    @classmethod
    def RegisterRefresh(cls, application) -> None:
        @application.callback(
            Output("server-state", "children"),
            Output("server-host", "children"),
            Output("server-uptime", "children"),
            Output("server-clients", "children"),
            Output("client-chart", "figure"),
            Output("client-table", "children"),
            Output("database-info", "children"),
            Output("alert-banner", "children"),
            Input("refresh", "n_intervals"),
        )
        def Refresh(interval):
            Bridge.Record()
            status = Bridge.Status()
            database = Bridge.Database()

            state = "🟢 Running" if status["active"] else "🔴 Stopped"
            host = f"{status['host']}:{status['port']}"
            uptime = Panel.FormatUptime(status["uptime"])
            clients = str(status["clients"])

            figure = cls.BuildChart()
            table = cls.BuildTable(Bridge.Clients())
            dbinfo = cls.BuildDatabase(database)
            alert = cls.BuildAlert(Bridge.alert)

            return state, host, uptime, clients, figure, table, dbinfo, alert

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
                return Bridge.alert

            Bridge.Notify(message)
            prefix = "✅" if success else "⚠️"
            return f"{prefix} {message}"

    @classmethod
    def RegisterDatabase(cls, application) -> None:
        @application.callback(
            Output("database-message", "children"),
            Input("btn-db-connect", "n_clicks"),
            Input("btn-db-test", "n_clicks"),
            Input("btn-db-disconnect", "n_clicks"),
            prevent_initial_call=True,
        )
        def DatabaseAction(connect, test, disconnect):
            trigger = cls.Trigger()

            if trigger == "btn-db-connect":
                success, message = Engine.ConnectDirect()
                if success:
                    Database.Enabled = True
            elif trigger == "btn-db-test":
                success, message = Engine.Test()
            elif trigger == "btn-db-disconnect":
                Engine.Disconnect()
                Database.Enabled = False
                success, message = True, "Database disconnected."
            else:
                return ""

            prefix = "✅" if success else "⚠️"
            return f"{prefix} {message}"

    @staticmethod
    def Trigger() -> str:
        from dash import ctx

        if not ctx.triggered:
            return ""

        return ctx.triggered_id or ""

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
                line={"color": "#00bc8c", "width": 2},
                marker={"size": 6},
                name="Clients",
            )
        )

        figure.update_layout(
            template="plotly_dark",
            margin={"l": 40, "r": 20, "t": 20, "b": 40},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis={"title": "Time"},
            yaxis={"title": "Clients", "rangemode": "tozero"},
            height=320,
        )

        return figure

    @classmethod
    def BuildTable(cls, clients: list[str]):
        if not clients:
            return dbc.Alert("No clients connected.", color="secondary")

        rows = [
            html.Tr([html.Th("#"), html.Th("Address")]),
        ]

        for index, address in enumerate(clients, start=1):
            rows.append(html.Tr([html.Td(str(index)), html.Td(address)]))

        return dbc.Table(
            [html.Thead(rows[0]), html.Tbody(rows[1:])],
            bordered=True,
            hover=True,
            responsive=True,
            className="mb-0",
        )

    @classmethod
    def BuildDatabase(cls, database: dict):
        enabled = "Yes" if database["enabled"] else "No"
        active = "Connected" if database["active"] else "Disconnected"

        return html.Ul(
            [
                html.Li(f"Type: MySQL"),
                html.Li(f"Enabled: {enabled}"),
                html.Li(f"Status: {active}"),
                html.Li(f"Host: {database['host']}:{database['port']}"),
                html.Li(f"Database: {database['name']}"),
            ],
            className="mb-0",
        )

    @classmethod
    def BuildAlert(cls, message: str):
        if not message:
            return ""

        color = "success" if message.startswith("✅") or "started" in message.lower() else "info"

        if "fail" in message.lower() or "error" in message.lower() or "⚠️" in message:
            color = "warning"

        return dbc.Alert(message, color=color, className="mb-0")
