from cli.Arguments import Arguments
from cli.Menu import Menu
from cli.Terminal import Terminal
from config.Settings import ResolveHost
from config.Settings import Settings as Network
from config.Store import Store
from database.Engine import Engine
from database.Settings import Settings as Database
from hooks.Shutdown import Shutdown
from logger.Logger import Logger
from network.Server import Server


def Main() -> None:
    arguments = Arguments.Parse()
    Store.Load()
    Logger.Initialize(level=arguments.level)

    logger = Logger.Get("Main")

    if arguments.headless:
        RunHeadless(arguments, logger)
    elif arguments.dash:
        RunDash(arguments, logger)
    else:
        RunPanel(logger)


def RunHeadless(arguments, logger) -> None:
    host = arguments.host if arguments.host else ResolveHost()
    port = Network.Port

    logger.info(
        "Starting Dicer server | host=%s | port=%d | level=%s",
        host,
        port,
        arguments.level,
    )

    if Database.Enabled:
        success, message = Engine.Connect()
        logger.info("Database connect | success=%s | message=%s", success, message)

    server = Server(host=host, port=port)

    Shutdown.Register(server)
    server.Start()

    Engine.Disconnect()


def RunPanel(logger) -> None:
    Terminal.Configure()

    logger.info("Opening management panel")

    Menu.Run()


def RunDash(arguments, logger) -> None:
    from board.App import App
    from board.Settings import Settings as Board
    from cli.Manager import Manager

    host = arguments.dash_host or Board.Host
    port = arguments.dash_port or Board.Port

    logger.info("Opening Dash dashboard | host=%s | port=%d", host, port)

    manager = Manager()
    App.Run(manager, host=host, port=port)


if __name__ == "__main__":
    Main()
