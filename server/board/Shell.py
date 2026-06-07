import dash_bootstrap_components as dbc
from dash import dcc, html

from board.Widgets import Widgets
from board.screens.Pages import Clients
from board.screens.Pages import Dashboard
from board.screens.Pages import Settings
from board.screens.Pages import Users
from board.Settings import Settings as Panel


class Shell:
    # Main application shell with sidebar navigation and page panels.

    NavMain = [
        ("dashboard", "bi-speedometer2", "Dashboard"),
        ("clients", "bi-people", "Clients"),
        ("users", "bi-person-badge", "Users"),
    ]

    NavSettings = [
        ("network", "bi-hdd-network", "Network"),
        ("logging", "bi-journal-text", "Logging"),
        ("connection", "bi-plug", "Connection"),
        ("security", "bi-shield-lock", "Security"),
        ("database", "bi-database", "Database"),
        ("mail", "bi-envelope", "Mail"),
        ("storage", "bi-save", "Storage"),
        ("panel", "bi-sliders", "Panel"),
    ]

    Titles = {
        "dashboard": "Dashboard",
        "clients": "Clients",
        "users": "Users",
        "network": "Network Settings",
        "logging": "Logging Settings",
        "connection": "Connection Settings",
        "security": "Security Settings",
        "database": "Database Settings",
        "mail": "Mail Settings",
        "storage": "Save / Load / Reset",
        "panel": "Panel Settings",
    }

    Subtitles = {
        "dashboard": "Live server overview",
        "clients": "Active TCP connections",
        "users": "Registered accounts stored in MySQL",
        "network": "Listen address, port, and limits",
        "logging": "Console and file output",
        "connection": "Welcome message and buffers",
        "security": "Password and IP filtering",
        "database": "MySQL connection settings",
        "mail": "SMTP delivery for verification codes",
        "storage": "Persist settings to disk",
        "panel": "Web dashboard preferences",
    }

    Pages = [
        "dashboard",
        "clients",
        "users",
        "network",
        "logging",
        "connection",
        "security",
        "database",
        "mail",
        "storage",
        "panel",
    ]

    @classmethod
    def Build(cls):
        pages = [Dashboard.Build(), Clients.Build(), Users.Build(), *Settings.Build()]

        return html.Div(
            [
                dcc.Store(id="page", data="dashboard"),
                dcc.Interval(id="refresh", interval=Panel.Interval, n_intervals=0),
                html.Div(
                    className="app-shell",
                    children=[
                        cls.Sidebar(),
                        html.Div(
                            className="app-main",
                            children=[
                                cls.Topbar(),
                                html.Div(
                                    id="alert-banner",
                                    className="px-4 pt-3",
                                ),
                                html.Div(
                                    className="app-content",
                                    children=pages,
                                ),
                            ],
                        ),
                    ],
                ),
            ]
        )

    @classmethod
    def Sidebar(cls):
        return html.Div(
            className="app-sidebar",
            children=[
                html.Div(
                    className="sidebar-brand",
                    children=[
                        html.H4("🎲 Dicer"),
                        html.Small("Server Control Panel"),
                    ],
                ),
                html.Div("Main", className="sidebar-section"),
                cls.Links(cls.NavMain),
                html.Div("Settings", className="sidebar-section"),
                cls.Links(cls.NavSettings),
                html.Div(
                    className="mt-auto p-3",
                    children=[
                        html.Small(
                            "Dash 4.x · Plotly",
                            className="text-muted",
                        ),
                    ],
                ),
            ],
        )

    @classmethod
    def Links(cls, items: list[tuple[str, str, str]]):
        return html.Div(
            [
                html.A(
                    [html.I(className=f"bi {icon}"), label],
                    id=f"nav-{page}",
                    className="sidebar-link" + (" active" if page == "dashboard" else ""),
                    n_clicks=0,
                )
                for page, icon, label in items
            ]
        )

    @classmethod
    def Topbar(cls):
        return html.Div(
            className="app-topbar",
            children=[
                html.Div(
                    [
                        html.H5(id="topbar-title", children="Dashboard", className="mb-0"),
                        html.Small(
                            id="topbar-subtitle",
                            children="Live server overview",
                            className="text-muted",
                        ),
                    ]
                ),
                html.Div(
                    [
                        Widgets.StatusPill("topbar-status"),
                        html.Span(id="topbar-clock", className="text-muted ms-3 small"),
                    ],
                    className="d-flex align-items-center",
                ),
            ],
        )
