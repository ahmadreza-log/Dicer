import logging


class Format:
    # Full detail pattern: timestamp, level, source location, thread, and message.
    Pattern = (
        "%(asctime)s.%(msecs)03d"
        " | %(levelname)-8s"
        " | %(name)s:%(funcName)s:%(lineno)d"
        " | %(threadName)s"
        " | %(message)s"
    )

    # ISO-style date used in every log line.
    DatePattern = "%Y-%m-%d %H:%M:%S"

    # Builds a formatter with the standard Dicer log layout.
    @staticmethod
    def Create() -> logging.Formatter:
        return logging.Formatter(
            fmt=Format.Pattern,
            datefmt=Format.DatePattern,
        )
