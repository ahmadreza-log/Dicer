class Locale:
    # Translation facade. Register language packs in i18n/Catalog.py.

    DefaultCode = "en"
    Code = DefaultCode
    _packs: dict[str, dict] = {}

    @classmethod
    def Register(cls, code: str, label: str, strings: dict[str, str], rtl: bool = False) -> None:
        cls._packs[code] = {
            "label": label,
            "strings": strings,
            "rtl": rtl,
        }

    @classmethod
    def LoadCatalog(cls) -> None:
        if cls._packs:
            return

        from i18n.Catalog import RegisterAll

        RegisterAll()

    @classmethod
    def Normalize(cls, code: str) -> str:
        cls.LoadCatalog()

        if code in cls._packs:
            return code

        return cls.DefaultCode

    @classmethod
    def Set(cls, code: str) -> bool:
        cls.LoadCatalog()
        resolved = cls.Normalize(code)

        if resolved not in cls._packs:
            return False

        cls.Code = resolved
        return True

    @classmethod
    def IsRtl(cls) -> bool:
        cls.LoadCatalog()
        pack = cls._packs.get(cls.Code, cls._packs[cls.DefaultCode])
        return bool(pack.get("rtl"))

    @classmethod
    def t(cls, key: str, **kwargs) -> str:
        cls.LoadCatalog()

        current = cls._packs.get(cls.Code, cls._packs[cls.DefaultCode])["strings"]
        fallback = cls._packs[cls.DefaultCode]["strings"]
        text = current.get(key, fallback.get(key, key))

        if kwargs:
            return text.format(**kwargs)

        return text

    @classmethod
    def Choices(cls) -> list[tuple[str, str]]:
        cls.LoadCatalog()
        return [(code, meta["label"]) for code, meta in cls._packs.items()]
