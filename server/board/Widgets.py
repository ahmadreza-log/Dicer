import dash_bootstrap_components as dbc
from dash import dcc, html


class Widgets:
    # Reusable dashboard widgets for the Dash panel.

    @classmethod
    def Metric(cls, identifier: str, label: str, icon: str, accent: str = ""):
        return dbc.Card(
            dbc.CardBody(
                [
                    html.I(className=f"bi {icon} metric-icon"),
                    html.P(label, className="metric-label"),
                    html.H3("—", id=identifier, className="metric-value"),
                ]
            ),
            className=f"metric-card {accent}".strip(),
        )

    @classmethod
    def PageHeader(cls, title: str, subtitle: str = ""):
        return html.Div(
            [
                html.H3(title, className="mb-1"),
                html.P(subtitle, className="text-muted mb-4") if subtitle else None,
            ]
        )

    @classmethod
    def Panel(cls, title: str, body, extra_class: str = ""):
        return dbc.Card(
            [
                dbc.CardHeader(title),
                dbc.CardBody(body),
            ],
            className=f"panel-card {extra_class}".strip(),
        )

    @classmethod
    def ControlBar(cls):
        return dbc.ButtonGroup(
            [
                dbc.Button("▶️ Start", id="btn-start", color="success", className="me-2"),
                dbc.Button("⏹️ Stop", id="btn-stop", color="danger", className="me-2"),
                dbc.Button("🔄 Restart", id="btn-restart", color="warning"),
            ],
            className="mb-0",
        )

    @classmethod
    def Chart(cls, identifier: str = "client-chart", height: int = 320):
        return dcc.Graph(id=identifier, config={"displayModeBar": False})

    @classmethod
    def StatusPill(cls, identifier: str = "topbar-status"):
        return html.Span(
            id=identifier,
            className="status-pill stopped",
            children=["● ", "Stopped"],
        )
