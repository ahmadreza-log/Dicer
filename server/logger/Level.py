import logging


class Level:
    # Converts a human-readable level name into the numeric value used by the logging module.
    @staticmethod
    def Parse(name: str) -> int:
        numeric = getattr(logging, name.upper(), None)

        if isinstance(numeric, int):
            return numeric

        return logging.INFO
