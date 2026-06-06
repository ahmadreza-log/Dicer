# Logging configuration for the Dicer central server.
# Adjust these values to control verbosity, output targets, and file rotation.


class Settings:
    # Master switch for the entire logging system.
    # Set to True when logging development is complete and ready for use.
    Enabled = False

    # Minimum severity level written to handlers (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    Level = "INFO"

    # Folder name (inside server/) where log files are stored.
    Directory = "logs"

    # Primary log file name inside the logs directory.
    Filename = "dicer.log"

    # Maximum size of a single log file in bytes before rotation occurs.
    MaxBytes = 5 * 1024 * 1024

    # Number of rotated backup files to keep on disk.
    Backups = 5

    # Whether log output is also printed to the terminal.
    Console = True

    # Whether log output is persisted to a file on disk.
    File = True
