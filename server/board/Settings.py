# Dash web dashboard settings for the Dicer central server.
# Uses Plotly Dash 4.x (https://dash.plotly.com).


class Settings:
    # Address the Dash dashboard binds to (local only by default).
    Host = "127.0.0.1"

    # HTTP port for the management dashboard.
    Port = 8050

    # Enable Dash debug mode (disable in production).
    Debug = False

    # Auto-refresh interval for live status widgets (milliseconds).
    Interval = 2000
