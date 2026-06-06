import secrets
import string


class Id:
    # Generates a short alphanumeric room identifier.

    Alphabet = string.ascii_letters + string.digits

    @classmethod
    def Generate(cls, length: int = 10) -> str:
        return "".join(secrets.choice(cls.Alphabet) for _ in range(length))
