from App import App
from Store import Store


def Main() -> None:
    Store.Load()
    application = App()
    application.Run()


if __name__ == "__main__":
    Main()
