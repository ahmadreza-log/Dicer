import dash_bootstrap_components as dbc
from dash import html

from cli.settings.Summary import Summary


class Overview:
    # Builds categorized settings overview boxes for the Storage page.

    Icons = {
        "Network": "bi-hdd-network",
        "Logging": "bi-journal-text",
        "Connection": "bi-plug",
        "Security": "bi-shield-lock",
        "Database": "bi-database",
        "Storage": "bi-save",
        "Panel": "bi-sliders",
        "Runtime": "bi-cpu",
    }

    @classmethod
    def Build(cls, manager) -> html.Div:
        if manager is None:
            return html.P("Loading…", className="text-muted mb-0")

        sections = cls.Parse(Summary.AllRows(manager))

        return dbc.Row(
            [
                dbc.Col(cls.Box(section), md=6, xl=4, className="d-flex")
                for section in sections
            ],
            className="g-3",
        )

    @classmethod
    def Parse(cls, rows: list[tuple[str, str]]) -> list[dict]:
        sections: list[dict] = []
        current: dict | None = None

        for label, value in rows:
            if label.startswith("──"):
                title = label.strip("─ ").strip()
                current = {"title": title, "rows": []}
                sections.append(current)
                continue

            if current is not None:
                clean = label.rstrip(":").strip()
                current["rows"].append((clean, value or "—"))

        return sections

    @classmethod
    def Box(cls, section: dict):
        title = section["title"]
        icon = cls.Icons.get(title, "bi-gear")

        return dbc.Card(
            [
                dbc.CardHeader(
                    html.Div(
                        [
                            html.I(className=f"bi {icon} me-2"),
                            title,
                        ],
                        className="d-flex align-items-center",
                    )
                ),
                dbc.CardBody(
                    [cls.Row(label, value) for label, value in section["rows"]],
                    className="overview-body",
                ),
            ],
            className="panel-card overview-box w-100",
        )

    @classmethod
    def Row(cls, label: str, value: str):
        return html.Div(
            [
                html.Span(label, className="overview-label"),
                html.Span(value, className="overview-value"),
            ],
            className="overview-row",
        )
