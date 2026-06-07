# Server connection settings for the Dicer client.


class Settings:
    DefaultHost = "127.0.0.1"
    Port = 12055
    Timeout = 5

    Host = DefaultHost

    @classmethod
    def Endpoint(cls) -> str:
        return f"{cls.Host}:{cls.Port}"

    @classmethod
    def ApplyHost(cls, host: str) -> None:
        cls.Host = host.strip()

    @classmethod
    def ValidateHost(cls, host: str) -> tuple[bool, str]:
        host = host.strip()

        if not host:
            return False, "network.error.empty_host"

        return True, ""

    @classmethod
    def Reset(cls) -> None:
        cls.ApplyHost(cls.DefaultHost)
