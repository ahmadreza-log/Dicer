import dash_bootstrap_components as dbc
from dash import dcc, html

from board.Settings import Settings as Board
from config.Settings import Settings as Network
from connection.Settings import Settings as Connection
from database.Settings import Settings as Database
from logger.Settings import Settings as Logging
from mail.Settings import Settings as Mail
from security.Settings import Settings as Security


class Forms:
    # Settings form builders for the Dash panel.

    @classmethod
    def Actions(cls, prefix: str, extra: list | None = None):
        buttons = [
            dbc.Button(
                "💾 Apply",
                id=f"btn-{prefix}-apply",
                color="success",
                className="me-2",
            ),
        ]

        if extra:
            buttons.extend(extra)

        return dbc.Row(
            dbc.Col(dbc.ButtonGroup(buttons), className="mt-3"),
        )

    @classmethod
    def Network(cls):
        return html.Div(
            className="settings-form",
            children=[
                dbc.Form(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Listen Mode"),
                                        dbc.Select(
                                            id="set-net-mode",
                                            options=[
                                                {"label": "Local (127.0.0.1)", "value": "Local"},
                                                {"label": "Network (0.0.0.0)", "value": "Network"},
                                                {"label": "Custom Host", "value": "Custom"},
                                            ],
                                        ),
                                    ],
                                    md=6,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Custom Host"),
                                        dbc.Input(id="set-net-host", placeholder="127.0.0.1"),
                                    ],
                                    md=6,
                                ),
                            ],
                            className="mb-3 g-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Max Clients (0 = unlimited)"),
                                        dbc.Input(id="set-net-max", type="number", min=0),
                                    ],
                                    md=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Auto Start"),
                                        dbc.Checklist(
                                            id="set-net-auto",
                                            options=[{"label": " Start server on launch", "value": "yes"}],
                                            switch=True,
                                        ),
                                    ],
                                    md=4,
                                    className="d-flex flex-column justify-content-end",
                                ),
                                dbc.Col(
                                    dbc.Alert(
                                        f"TCP port {Network.Port} is fixed and cannot be changed.",
                                        color="secondary",
                                        className="mb-0 py-2",
                                    ),
                                    md=4,
                                    className="d-flex align-items-end",
                                ),
                            ],
                            className="mb-2 g-3",
                        ),
                    ],
                ),
                cls.Actions("net"),
                html.Div(id="set-net-message", className="mt-3"),
            ],
        )

    @classmethod
    def Logging(cls):
        return html.Div(
            className="settings-form",
            children=[
                dbc.Form(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Checklist(
                                        id="set-log-enabled",
                                        options=[{"label": " Enable logging", "value": "yes"}],
                                        switch=True,
                                    ),
                                    md=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Level"),
                                        dbc.Select(
                                            id="set-log-level",
                                            options=[
                                                {"label": level, "value": level}
                                                for level in (
                                                    "DEBUG",
                                                    "INFO",
                                                    "WARNING",
                                                    "ERROR",
                                                    "CRITICAL",
                                                )
                                            ],
                                        ),
                                    ],
                                    md=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Directory"),
                                        dbc.Input(id="set-log-dir"),
                                    ],
                                    md=4,
                                ),
                            ],
                            className="mb-3 g-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Checklist(
                                        id="set-log-console",
                                        options=[{"label": " Console output", "value": "yes"}],
                                        switch=True,
                                    ),
                                    md=3,
                                ),
                                dbc.Col(
                                    dbc.Checklist(
                                        id="set-log-file",
                                        options=[{"label": " File output", "value": "yes"}],
                                        switch=True,
                                    ),
                                    md=3,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Filename"),
                                        dbc.Input(id="set-log-name"),
                                    ],
                                    md=3,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Max Size (MB)"),
                                        dbc.Input(id="set-log-size", type="number", min=1),
                                    ],
                                    md=3,
                                ),
                            ],
                            className="mb-3 g-3",
                        ),
                        dbc.Row(
                            dbc.Col(
                                [
                                    dbc.Label("Rotated Backups"),
                                    dbc.Input(id="set-log-backups", type="number", min=0),
                                ],
                                md=4,
                            ),
                            className="g-3",
                        ),
                    ],
                ),
                cls.Actions("log"),
                html.Div(id="set-log-message", className="mt-3"),
            ],
        )

    @classmethod
    def Connection(cls):
        return html.Div(
            className="settings-form",
            children=[
                dbc.Form(
                    [
                        dbc.Row(
                            dbc.Col(
                                [
                                    dbc.Label("Welcome Message"),
                                    dbc.Textarea(id="set-con-welcome", rows=2),
                                ],
                            ),
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Buffer Size (bytes)"),
                                        dbc.Input(id="set-con-buffer", type="number", min=256),
                                    ],
                                    md=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Idle Timeout (seconds, 0 = off)"),
                                        dbc.Input(id="set-con-timeout", type="number", min=0),
                                    ],
                                    md=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Max Connections / IP (0 = unlimited)"),
                                        dbc.Input(id="set-con-max", type="number", min=0),
                                    ],
                                    md=4,
                                ),
                            ],
                            className="g-3",
                        ),
                    ],
                ),
                cls.Actions("con"),
                html.Div(id="set-con-message", className="mt-3"),
            ],
        )

    @classmethod
    def Security(cls):
        return html.Div(
            className="settings-form",
            children=[
                dbc.Form(
                    [
                        dbc.Row(
                            dbc.Col(
                                [
                                    dbc.Label("Server Password (empty = disabled)"),
                                    dbc.Input(id="set-sec-pass", type="password"),
                                ],
                            ),
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Allowed IPs (comma-separated, empty = all)"),
                                        dbc.Textarea(id="set-sec-allowed", rows=2),
                                    ],
                                    md=6,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Blocked IPs (comma-separated)"),
                                        dbc.Textarea(id="set-sec-blocked", rows=2),
                                    ],
                                    md=6,
                                ),
                            ],
                            className="g-3",
                        ),
                    ],
                ),
                cls.Actions("sec"),
                html.Div(id="set-sec-message", className="mt-3"),
            ],
        )

    @classmethod
    def Database(cls):
        return html.Div(
            className="settings-form",
            children=[
                dbc.Alert(
                    f"Engine: {Database.Type} — only MySQL is supported today.",
                    color="info",
                    className="mb-3",
                ),
                dbc.Form(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Checklist(
                                        id="set-db-enabled",
                                        options=[{"label": " Enable database", "value": "yes"}],
                                        switch=True,
                                    ),
                                    md=12,
                                    className="mb-3",
                                ),
                            ],
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [dbc.Label("Host"), dbc.Input(id="set-db-host")],
                                    md=3,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Port"),
                                        dbc.Input(id="set-db-port", type="number", min=1, max=65535),
                                    ],
                                    md=2,
                                ),
                                dbc.Col(
                                    [dbc.Label("User"), dbc.Input(id="set-db-user")],
                                    md=2,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Password"),
                                        dbc.Input(id="set-db-pass", type="password"),
                                    ],
                                    md=2,
                                ),
                                dbc.Col(
                                    [dbc.Label("Database Name"), dbc.Input(id="set-db-name")],
                                    md=3,
                                ),
                            ],
                            className="g-3 mb-2",
                        ),
                    ],
                ),
                cls.Actions(
                    "db",
                    extra=[
                        dbc.Button("🧪 Test", id="btn-db-test", color="info", className="me-2"),
                        dbc.Button("🔗 Connect", id="btn-db-connect", color="primary", className="me-2"),
                        dbc.Button("⏹️ Disconnect", id="btn-db-disconnect", color="secondary"),
                    ],
                ),
                html.Div(id="set-db-message", className="mt-3"),
            ],
        )

    @classmethod
    def Mail(cls):
        return html.Div(
            children=[
                dbc.Alert(
                    "In test mode, verification codes are written to the server console "
                    "and logs/test-mail.log. Enable SMTP only for real delivery.",
                    color="info",
                    className="mb-3",
                ),
                dbc.Form(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Checklist(
                                        id="set-mail-test",
                                        options=[
                                            {
                                                "label": " Test mode (log codes locally, no SMTP)",
                                                "value": "yes",
                                            }
                                        ],
                                        switch=True,
                                    ),
                                    md=12,
                                    className="mb-2",
                                ),
                                dbc.Col(
                                    dbc.Checklist(
                                        id="set-mail-enabled",
                                        options=[{"label": " Enable outbound email (SMTP)", "value": "yes"}],
                                        switch=True,
                                    ),
                                    md=12,
                                    className="mb-3",
                                ),
                            ],
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [dbc.Label("SMTP Host"), dbc.Input(id="set-mail-host")],
                                    md=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Port"),
                                        dbc.Input(id="set-mail-port", type="number", min=1, max=65535),
                                    ],
                                    md=2,
                                ),
                                dbc.Col(
                                    [dbc.Label("Username"), dbc.Input(id="set-mail-user")],
                                    md=3,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Password"),
                                        dbc.Input(id="set-mail-pass", type="password"),
                                    ],
                                    md=3,
                                ),
                            ],
                            className="g-3 mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [dbc.Label("From Address"), dbc.Input(id="set-mail-from")],
                                    md=4,
                                ),
                                dbc.Col(
                                    [dbc.Label("From Name"), dbc.Input(id="set-mail-from-name")],
                                    md=4,
                                ),
                                dbc.Col(
                                    dbc.Checklist(
                                        id="set-mail-tls",
                                        options=[{"label": " Use TLS", "value": "yes"}],
                                        switch=True,
                                        className="mt-4",
                                    ),
                                    md=4,
                                ),
                            ],
                            className="g-3",
                        ),
                    ],
                ),
                cls.Actions("mail"),
                html.Div(id="set-mail-message", className="mt-3"),
            ],
        )

    @classmethod
    def Storage(cls):
        return html.Div(
            children=[
                dbc.Row(
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("💾 Persist Settings", className="mb-3"),
                                    html.P(
                                        "Save current settings to config/stored.json. "
                                        "Load and Reset require the TCP server to be stopped.",
                                        className="text-muted small",
                                    ),
                                    dbc.ButtonGroup(
                                        [
                                            dbc.Button("Save", id="btn-store-save", color="success", className="me-2"),
                                            dbc.Button("Load", id="btn-store-load", color="primary", className="me-2"),
                                            dbc.Button("Reset Defaults", id="btn-store-reset", color="warning"),
                                        ],
                                    ),
                                    html.Div(id="set-store-message", className="mt-3"),
                                ]
                            ),
                            className="panel-card",
                        ),
                        lg=4,
                    ),
                    className="g-3 mb-4",
                ),
                html.H5("📋 All Settings Overview", className="mb-3"),
                html.Div(id="settings-overview"),
            ],
        )

    @classmethod
    def Board(cls):
        return html.Div(
            className="settings-form",
            children=[
                dbc.Alert(
                    "These settings affect the web dashboard only. Restart --dash to apply host/port changes.",
                    color="secondary",
                    className="mb-3",
                ),
                dbc.Form(
                    dbc.Row(
                        [
                            dbc.Col(
                                [dbc.Label("Dashboard Host"), dbc.Input(id="set-panel-host")],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Dashboard Port"),
                                    dbc.Input(id="set-panel-port", type="number", min=1, max=65535),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Refresh Interval (seconds)"),
                                    dbc.Input(id="set-panel-interval", type="number", min=1, step=1),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                dbc.Checklist(
                                    id="set-panel-debug",
                                    options=[{"label": " Debug mode", "value": "yes"}],
                                    switch=True,
                                    className="mt-4",
                                ),
                                md=3,
                            ),
                        ],
                        className="g-3",
                    ),
                ),
                cls.Actions("panel"),
                html.Div(id="set-panel-message", className="mt-3"),
            ],
        )

    @classmethod
    def Values(cls) -> dict:
        return {
            "net": {
                "mode": Network.Mode,
                "host": Network.Host,
                "max": Network.MaxClients,
                "auto": ["yes"] if Network.AutoStart else [],
            },
            "log": {
                "enabled": ["yes"] if Logging.Enabled else [],
                "level": Logging.Level,
                "console": ["yes"] if Logging.Console else [],
                "file": ["yes"] if Logging.File else [],
                "dir": Logging.Directory,
                "name": Logging.Filename,
                "size": Logging.MaxBytes // (1024 * 1024),
                "backups": Logging.Backups,
            },
            "con": {
                "welcome": Connection.Welcome,
                "buffer": Connection.Buffer,
                "timeout": Connection.Timeout,
                "max": Connection.MaxPerAddress,
            },
            "sec": {
                "pass": Security.Password,
                "allowed": Security.Allowed,
                "blocked": Security.Blocked,
            },
            "db": {
                "enabled": ["yes"] if Database.Enabled else [],
                "host": Database.Host,
                "port": Database.Port,
                "user": Database.User,
                "pass": Database.Password,
                "name": Database.Name,
            },
            "mail": {
                "test_mode": ["yes"] if Mail.TestMode else [],
                "enabled": ["yes"] if Mail.Enabled else [],
                "host": Mail.Host,
                "port": Mail.Port,
                "user": Mail.Username,
                "pass": Mail.Password,
                "from_address": Mail.FromAddress,
                "from_name": Mail.FromName,
                "tls": ["yes"] if Mail.UseTls else [],
            },
            "panel": {
                "host": Board.Host,
                "port": Board.Port,
                "interval": max(1, Board.Interval // 1000),
                "debug": ["yes"] if Board.Debug else [],
            },
        }
