import logging
import sys

from logger.Format import Format
from logger.Level import Level
from logger.Settings import Settings


class Console:
    # Creates a stream handler that writes formatted logs to the terminal.
    @staticmethod
    def Create() -> logging.StreamHandler:
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(Level.Parse(Settings.Level))
        handler.setFormatter(Format.Create())
        return handler
