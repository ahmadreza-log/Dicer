import logging

from logger.Console import Console
from logger.File import File
from logger.Level import Level
from logger.Settings import Settings


class Logger:
    # Central logging facade for the entire Dicer server application.
    # All modules should obtain a named logger through Get() instead of
    # calling the standard library logging module directly.

    Root = "Dicer"
    Initialized = False

    # Sets up console and file handlers with the configured log level.
    # Must be called once at application startup before any Get() calls.
    @classmethod
    def Initialize(cls, level: str | None = None) -> None:
        if cls.Initialized:
            return

        if level is not None:
            Settings.Level = level.upper()

        root = logging.getLogger(cls.Root)
        root.propagate = False
        root.handlers.clear()

        if not Settings.Enabled:
            root.addHandler(logging.NullHandler())
            root.setLevel(logging.CRITICAL + 1)
            cls.Initialized = True
            return

        root.setLevel(Level.Parse(Settings.Level))

        if Settings.Console:
            root.addHandler(Console.Create())

        if Settings.File:
            root.addHandler(File.Create())

        cls.Initialized = True
        logger = cls.Get("Logger")
        logger.info(
            "Logging initialized | level=%s | console=%s | file=%s | directory=%s",
            Settings.Level,
            Settings.Console,
            Settings.File,
            Settings.Directory,
        )

    # Rebuilds handlers after settings are changed at runtime.
    @classmethod
    def Reset(cls) -> None:
        cls.Initialized = False
        cls.Initialize()

    # Returns a named child logger under the Dicer root namespace.
    @classmethod
    def Get(cls, name: str) -> logging.Logger:
        if not cls.Initialized:
            cls.Initialize()

        return logging.getLogger(f"{cls.Root}.{name}")
