from App import App
from i18n.Locale import Locale
from Store import Store


def Main() -> None:
    Store.Load()
    Locale.LoadCatalog()
    Locale.Set(Store.LocaleCode)

    application = App()
    application.Run()


if __name__ == "__main__":
    Main()
