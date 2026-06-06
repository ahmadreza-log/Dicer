import dash_bootstrap_components as dbc
from dash import dcc, html

from board.Settings import Settings


class Layout:
    # Builds the Dash dashboard layout (Plotly Dash 4.x + Bootstrap).

    @classmethod
    def Build(cls):
        return dbc.Container(
            fluid=True,
            className="py-4",
            children=[
                cls.Header(),
                html.Div(id="alert-banner", className="mb-3"),
                dcc.Interval(
                    id="refresh",
                    interval=Settings.Interval,
                    n_intervals=0,
                ),
                dbc.Row(
                    [
                        dbc.Col(cls.StatusCards(), lg=8),
                        dbc.Col(cls.ControlPanel(), lg=4),
                    ],
                    className="mb-4 g-3",
                ),
                dbc.Row(
                    [
                        dbc.Col(cls.ClientChart(), lg=7),
                        dbc.Col(cls.ClientTable(), lg=5),
                    ],
                    className="mb-4 g-3",
                ),
                dbc.Row(
                    [
                        dbc.Col(cls.DatabasePanel(), lg=12),
                    ],
                    className="g-3",
                ),
            ],
        )

    @classmethod
    def Header(cls):
        return dbc.Navbar(
            dbc.Container(
                [
                    dbc.NavbarBrand("🎲 Dicer Server Dashboard", className="fw-bold"),
                    dbc.Nav(
                        dbc.NavItem(
                            dbc.NavLink(
                                "Plotly Dash 4.x",
                                href="https://dash.plotly.com",
                                target="_blank",
                            )
                        ),
                        className="ms-auto",
                    ),
                ],
                fluid=True,
            ),
            color="dark",
            dark=True,
            className="mb-4 rounded",
        )

    @classmethod
    def StatusCards(cls):
        return dbc.Row(
            [
                dbc.Col(cls.Metric("server-state", "Server", "—"), md=3),
                dbc.Col(cls.Metric("server-host", "Host", "—"), md=3),
                dbc.Col(cls.Metric("server-uptime", "Uptime", "—"), md=3),
                dbc.Col(cls.Metric("server-clients", "Clients", "—"), md=3),
            ],
            className="g-3",
        )

    @classmethod
    def Metric(cls, identifier: str, label: str, value: str):
        return dbc.Card(
            dbc.CardBody(
                [
                    html.P(label, className="text-muted mb-1"),
                    html.H4(value, id=identifier, className="mb-0"),
                ]
            ),
            className="h-100 border-secondary",
        )

    @classmethod
    def ControlPanel(cls):
        return dbc.Card(
            [
                dbc.CardHeader("⚙️ Server Controls"),
                dbc.CardBody(
                    [
                        dbc.ButtonGroup(
                            [
                                dbc.Button(
                                    "▶️ Start",
                                    id="btn-start",
                                    color="success",
                                    className="me-2",
                                ),
                                dbc.Button(
                                    "⏹️ Stop",
                                    id="btn-stop",
                                    color="danger",
                                    className="me-2",
                                ),
                                dbc.Button(
                                    "🔄 Restart",
                                    id="btn-restart",
                                    color="warning",
                                ),
                            ],
                            className="w-100 mb-3",
                        ),
                        html.P(
                            id="control-message",
                            className="text-muted small mb-0",
                        ),
                    ]
                ),
            ],
            className="h-100 border-secondary",
        )

    @classmethod
    def ClientChart(cls):
        return dbc.Card(
            [
                dbc.CardHeader("📊 Connected Clients (Live)"),
                dbc.CardBody(dcc.Graph(id="client-chart")),
            ],
            className="border-secondary",
        )

    @classmethod
    def ClientTable(cls):
        return dbc.Card(
            [
                dbc.CardHeader("👥 Active Connections"),
                dbc.CardBody(html.Div(id="client-table")),
            ],
            className="border-secondary",
        )

    @classmethod
    def DatabasePanel(cls):
        return dbc.Card(
            [
                dbc.CardHeader("🗄️ Database (MySQL)"),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="database-info"), md=8),
                                dbc.Col(
                                    dbc.ButtonGroup(
                                        [
                                            dbc.Button(
                                                "🔗 Connect",
                                                id="btn-db-connect",
                                                color="primary",
                                                className="me-2",
                                            ),
                                            dbc.Button(
                                                "🧪 Test",
                                                id="btn-db-test",
                                                color="info",
                                                className="me-2",
                                            ),
                                            dbc.Button(
                                                "⏹️ Disconnect",
                                                id="btn-db-disconnect",
                                                color="secondary",
                                            ),
                                        ],
                                        className="w-100",
                                    ),
                                    md=4,
                                ),
                            ],
                            className="align-items-center",
                        ),
                        html.P(
                            id="database-message",
                            className="text-muted small mt-3 mb-0",
                        ),
                    ]
                ),
            ],
            className="border-secondary",
        )
