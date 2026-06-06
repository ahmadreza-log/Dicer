import signal
import sys

from logger.Logger import Logger
from network.Server import Server


class Shutdown:
    # Registers OS signal handlers so the server can shut down gracefully.

    @staticmethod
    def Register(server: Server) -> None:
        logger = Logger.Get("Shutdown")

        def Handle(signal_number, stack_frame) -> None:
            logger.info("Shutdown signal received | signal=%d", signal_number)
            server.Stop()
            logger.info("Shutdown complete")
            sys.exit(0)

        signal.signal(signal.SIGINT, Handle)

        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, Handle)

        logger.debug("Signal handlers registered | signals=SIGINT,SIGTERM")
