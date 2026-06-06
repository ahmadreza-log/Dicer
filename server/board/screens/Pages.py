import dash_bootstrap_components as dbc
from dash import html

from board.Forms import Forms
from board.Widgets import Widgets


class Dashboard:
    # Main overview screen with live metrics and controls.

    @classmethod
    def Build(cls):
        return html.Div(
            id="page-dashboard",
            className="page-panel",
            children=[
                Widgets.PageHeader(
                    "Dashboard",
                    "Live overview of your Dicer central server.",
                ),
                dbc.Row(
                    [
                        dbc.Col(Widgets.Metric("metric-state", "Server", "bi-hdd-network"), lg=3, md=6),
                        dbc.Col(Widgets.Metric("metric-host", "Bind Address", "bi-globe2"), lg=3, md=6),
                        dbc.Col(Widgets.Metric("metric-uptime", "Uptime", "bi-clock-history"), lg=3, md=6),
                        dbc.Col(Widgets.Metric("metric-clients", "Clients", "bi-people-fill"), lg=3, md=6),
                    ],
                    className="g-3 mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            Widgets.Panel(
                                "📊 Client Activity",
                                Widgets.Chart(),
                            ),
                            lg=8,
                        ),
                        dbc.Col(
                            [
                                Widgets.Panel(
                                    "⚙️ Quick Controls",
                                    [
                                        Widgets.ControlBar(),
                                        html.Div(id="control-message", className="text-muted small mt-3 mb-0"),
                                    ],
                                ),
                                Widgets.Panel(
                                    "🗄️ Database",
                                    html.Div(id="dash-db-summary"),
                                    extra_class="mt-3",
                                ),
                            ],
                            lg=4,
                        ),
                    ],
                    className="g-3 mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            Widgets.Panel("📜 Recent Activity", html.Div(id="activity-feed")),
                            lg=5,
                        ),
                        dbc.Col(
                            Widgets.Panel("👥 Connected Clients", html.Div(id="client-table")),
                            lg=7,
                        ),
                    ],
                    className="g-3",
                ),
            ],
        )


class Clients:
    # Dedicated clients screen with full connection list.

    @classmethod
    def Build(cls):
        return html.Div(
            id="page-clients",
            className="page-panel",
            style={"display": "none"},
            children=[
                Widgets.PageHeader(
                    "Clients",
                    "All active TCP connections to the central server.",
                ),
                Widgets.Panel(
                    "👥 Active Connections",
                    [
                        html.Div(id="clients-full-table"),
                        html.P(id="clients-count", className="text-muted small mt-3 mb-0"),
                    ],
                ),
            ],
        )


class Settings:
    # Settings screens mirroring the CLI settings hub.

    @classmethod
    def Page(cls, page_id: str, title: str, subtitle: str, form):
        return html.Div(
            id=f"page-{page_id}",
            className="page-panel",
            style={"display": "none"},
            children=[
                Widgets.PageHeader(title, subtitle),
                Widgets.Panel(f"⚙️ {title}", form),
            ],
        )

    @classmethod
    def Build(cls):
        return [
            cls.Page(
                "network",
                "Network",
                "TCP listen address, port, and client limits.",
                Forms.Network(),
            ),
            cls.Page(
                "logging",
                "Logging",
                "Console and file logging configuration.",
                Forms.Logging(),
            ),
            cls.Page(
                "connection",
                "Connection",
                "Welcome message, buffer, and per-IP limits.",
                Forms.Connection(),
            ),
            cls.Page(
                "security",
                "Security",
                "Password and IP allow/block lists.",
                Forms.Security(),
            ),
            cls.Page(
                "database",
                "Database",
                "MySQL connection settings and actions.",
                Forms.Database(),
            ),
            cls.Page(
                "storage",
                "Storage",
                "Save, load, and reset persisted settings.",
                Forms.Storage(),
            ),
            cls.Page(
                "panel",
                "Panel",
                "Web dashboard host, port, and refresh rate.",
                Forms.Board(),
            ),
        ]
