import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from logger.Format import Format
from logger.Level import Level
from logger.Settings import Settings


class File:
    # Creates a rotating file handler that persists logs under server/logs/.
    @staticmethod
    def Create() -> RotatingFileHandler:
        directory = Path(__file__).resolve().parent.parent / Settings.Directory
        directory.mkdir(parents=True, exist_ok=True)

        filepath = directory / Settings.Filename

        handler = RotatingFileHandler(
            filename=filepath,
            maxBytes=Settings.MaxBytes,
            backupCount=Settings.Backups,
            encoding="utf-8",
        )
        handler.setLevel(Level.Parse(Settings.Level))
        handler.setFormatter(Format.Create())
        return handler
