from i18n import en, fa
from i18n.Locale import Locale


def RegisterAll() -> None:
    # Register every language pack listed below.
    # To add a new language, create i18n/<code>.py and append it to Packages.
    Packages = (
        en,
        fa,
    )

    for package in Packages:
        Locale.Register(
            package.CODE,
            package.LABEL,
            package.STRINGS,
            getattr(package, "RTL", False),
        )
