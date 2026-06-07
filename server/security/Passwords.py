import hashlib
import secrets


class Passwords:
    # PBKDF2-SHA256 password hashing with per-user salt and constant-time verify.

    Algorithm = "pbkdf2_sha256"
    Iterations = 600_000
    SaltBytes = 16

    @classmethod
    def Hash(cls, plain: str) -> str:
        salt = secrets.token_hex(cls.SaltBytes)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            plain.encode("utf-8"),
            bytes.fromhex(salt),
            cls.Iterations,
        )
        return f"{cls.Algorithm}${cls.Iterations}${salt}${digest.hex()}"

    @classmethod
    def Verify(cls, plain: str, hashed: str) -> bool:
        if not plain or not hashed:
            return False

        try:
            algorithm, iterations, salt, digest = hashed.split("$", 3)
        except ValueError:
            return False

        if algorithm != cls.Algorithm:
            return False

        try:
            resolved = hashlib.pbkdf2_hmac(
                "sha256",
                plain.encode("utf-8"),
                bytes.fromhex(salt),
                int(iterations),
            )
        except (ValueError, TypeError):
            return False

        return secrets.compare_digest(resolved.hex(), digest)

    @classmethod
    def Preview(cls, hashed: str) -> str:
        if not hashed:
            return "—"

        if len(hashed) <= 20:
            return hashed

        return f"{hashed[:20]}…"
