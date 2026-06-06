import argparse

from config.Settings import Settings
from logger.Settings import Settings as LogSettings


class Arguments:
    # Builds the command-line interface and returns parsed values.
    @staticmethod
    def Parse() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Dicer central server")

        parser.add_argument(
            "--host",
            default=None,
            help=f"Override host address (default: from settings / {Settings.Host})",
        )

        parser.add_argument(
            "--port",
            type=int,
            default=None,
            help=f"Override TCP port (default: from settings / {Settings.Port})",
        )

        parser.add_argument(
            "--level",
            default=LogSettings.Level,
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help=f"Logging level (default: {LogSettings.Level})",
        )

        parser.add_argument(
            "--headless",
            action="store_true",
            help="Start the server directly without the management panel",
        )

        parser.add_argument(
            "--dash",
            action="store_true",
            help="Start the Plotly Dash web dashboard instead of the CLI panel",
        )

        parser.add_argument(
            "--dash-host",
            default=None,
            help="Override Dash bind address (default: from board/Settings.py)",
        )

        parser.add_argument(
            "--dash-port",
            type=int,
            default=None,
            help="Override Dash HTTP port (default: from board/Settings.py)",
        )

        return parser.parse_args()
