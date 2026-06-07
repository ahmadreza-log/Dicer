import re

from database.Engine import Engine
from database.activation_codes.Repository import Repository as ActivationCodes
from logger.Logger import Logger
from mail.Sender import Sender
from security.Passwords import Passwords


class Repository:
    # Registered accounts with hashed passwords and activation state.

    logger = Logger.Get("Users")
    UsernamePattern = re.compile(r"^[A-Za-z0-9_]{3,32}$")
    EmailPattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    @classmethod
    def Ensure(cls) -> tuple[bool, str]:
        if not Engine.IsActive():
            return False, "Database is not connected."

        try:
            cursor = Engine.driver.link.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(64) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    active TINYINT(1) NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,
                    UNIQUE KEY uq_users_username (username),
                    UNIQUE KEY uq_users_email (email),
                    INDEX idx_users_email (email)
                )
                """
            )
            cls._MigrateSchema(cursor)
            Engine.driver.link.commit()
            cursor.close()
            return True, ""
        except Exception as error:
            cls.logger.error("User schema failed | reason=%s", error)
            return False, f"Database error: {error}"

    @classmethod
    def List(cls) -> tuple[bool, str, list[dict]]:
        ready, reason = cls.Ensure()

        if not ready:
            return False, reason, []

        try:
            cursor = Engine.driver.link.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id, username, email, password, active, created_at
                FROM users
                ORDER BY id DESC
                """
            )
            rows = cursor.fetchall()
            cursor.close()
            return True, "", [cls._SerializeDashboard(row) for row in rows]
        except Exception as error:
            cls.logger.error("User list failed | reason=%s", error)
            return False, f"Database error: {error}", []

    @classmethod
    def Register(cls, username: str, email: str, password: str) -> tuple[bool, str, dict | None]:
        ready, reason = cls.Ensure()

        if not ready:
            return False, reason, None

        valid, reason = cls._ValidateCredentials(username, email, password)

        if not valid:
            return False, reason, None

        hashed = Passwords.Hash(password)

        try:
            cursor = Engine.driver.link.cursor()
            cursor.execute(
                """
                INSERT INTO users (username, email, password, active)
                VALUES (%s, %s, %s, 0)
                """,
                (username.strip(), email.strip().lower(), hashed),
            )
            user_id = cursor.lastrowid
            Engine.driver.link.commit()
            cursor.close()
        except Exception as error:
            cls.logger.error("User register failed | username=%s | reason=%s", username, error)
            message = str(error).lower()

            if "duplicate" in message and "username" in message:
                return False, "Username is already taken.", None

            if "duplicate" in message and "email" in message:
                return False, "Email is already registered.", None

            return False, f"Database error: {error}", None

        issued, issue_reason, code = ActivationCodes.Issue(user_id)

        if not issued:
            cls.Delete(user_id)
            return False, issue_reason, None

        sent, send_reason = Sender.SendActivationCode(email, username, code)

        if not sent:
            cls.Delete(user_id)
            return False, send_reason or "Could not send verification email.", None

        user = cls.GetById(user_id)
        cls.logger.info("User registered | id=%s | username=%s", user_id, username)
        return True, "", user

    @classmethod
    def VerifyEmail(cls, user_id: int, code: str) -> tuple[bool, str, dict | None]:
        user = cls.GetById(user_id)

        if user is None:
            return False, "User not found.", None

        if user["active"]:
            return True, "", user

        valid, reason = ActivationCodes.Verify(user_id, code)

        if not valid:
            return False, reason, None

        try:
            cursor = Engine.driver.link.cursor()
            cursor.execute(
                """
                UPDATE users
                SET active = 1, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (user_id,),
            )
            Engine.driver.link.commit()
            cursor.close()
        except Exception as error:
            cls.logger.error("User verify failed | id=%s | reason=%s", user_id, error)
            return False, f"Database error: {error}", None

        verified = cls.GetById(user_id)
        cls.logger.info("User activated | id=%s", user_id)
        return True, "", verified

    @classmethod
    def ResendActivation(cls, user_id: int) -> tuple[bool, str]:
        user = cls.GetById(user_id)

        if user is None:
            return False, "User not found."

        if user["active"]:
            return False, "Email is already verified."

        issued, reason, code = ActivationCodes.Issue(user_id)

        if not issued:
            return False, reason

        sent, send_reason = Sender.SendActivationCode(user["email"], user["username"], code)

        if not sent:
            return False, send_reason or "Could not send verification email."

        return True, ""

    @classmethod
    def GetById(cls, user_id: int) -> dict | None:
        if not Engine.IsActive():
            return None

        try:
            cursor = Engine.driver.link.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id, username, email, password, active, created_at, updated_at
                FROM users
                WHERE id = %s
                LIMIT 1
                """,
                (user_id,),
            )
            row = cursor.fetchone()
            cursor.close()

            if row is None:
                return None

            return cls._Serialize(row)
        except Exception as error:
            cls.logger.error("User fetch failed | id=%s | reason=%s", user_id, error)
            return None

    @classmethod
    def Authenticate(cls, login: str, password: str) -> tuple[bool, str, dict | None]:
        ready, reason = cls.Ensure()

        if not ready:
            return False, reason, None

        resolved = login.strip()

        if not resolved or not password:
            return False, "Username and password are required.", None

        row = cls._FetchRow(resolved)

        if row is None or not Passwords.Verify(password, row.get("password") or ""):
            return False, "Invalid username or password.", None

        user = cls._Serialize(row)
        cls.logger.info("User authenticated | id=%s | username=%s", user["id"], user["username"])
        return True, "", user

    @classmethod
    def GetByUsername(cls, username: str) -> dict | None:
        if not username or not Engine.IsActive():
            return None

        row = cls._FetchRow(username.strip())

        if row is None:
            return None

        return cls._Serialize(row)

    @classmethod
    def GetByEmail(cls, email: str) -> dict | None:
        if not email or not Engine.IsActive():
            return None

        try:
            cursor = Engine.driver.link.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id, username, email, password, active, created_at, updated_at
                FROM users
                WHERE email = %s
                LIMIT 1
                """,
                (email.strip().lower(),),
            )
            row = cursor.fetchone()
            cursor.close()

            if row is None:
                return None

            return cls._Serialize(row)
        except Exception as error:
            cls.logger.error("User fetch failed | email=%s | reason=%s", email, error)
            return None

    @classmethod
    def Delete(cls, user_id: int) -> None:
        if not Engine.IsActive():
            return

        try:
            cursor = Engine.driver.link.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            Engine.driver.link.commit()
            cursor.close()
        except Exception as error:
            cls.logger.error("User delete failed | id=%s | reason=%s", user_id, error)

    @classmethod
    def _FetchRow(cls, login: str) -> dict | None:
        if not Engine.IsActive():
            return None

        resolved = login.strip()
        lookup = resolved.lower() if "@" in resolved else resolved
        column = "email" if "@" in resolved else "username"

        try:
            cursor = Engine.driver.link.cursor(dictionary=True)
            cursor.execute(
                f"""
                SELECT id, username, email, password, active, created_at, updated_at
                FROM users
                WHERE {column} = %s
                LIMIT 1
                """,
                (lookup,),
            )
            row = cursor.fetchone()
            cursor.close()
            return row
        except Exception as error:
            cls.logger.error("User fetch failed | login=%s | reason=%s", login, error)
            return None

    @classmethod
    def _ValidateCredentials(cls, username: str, email: str, password: str) -> tuple[bool, str]:
        resolved_username = username.strip()
        resolved_email = email.strip().lower()

        if not cls.UsernamePattern.fullmatch(resolved_username):
            return False, "Username must be 3-32 characters (letters, numbers, underscore)."

        if not cls.EmailPattern.fullmatch(resolved_email):
            return False, "Enter a valid email address."

        if len(password) < 8:
            return False, "Password must be at least 8 characters."

        if not any(character.isalpha() for character in password):
            return False, "Password must include at least one letter."

        if not any(character.isdigit() for character in password):
            return False, "Password must include at least one number."

        return True, ""

    @classmethod
    def _MigrateSchema(cls, cursor) -> None:
        if cls._ColumnExists(cursor, "password_hash") and not cls._ColumnExists(cursor, "password"):
            cursor.execute("ALTER TABLE users CHANGE password_hash password VARCHAR(255) NULL")

        if cls._ColumnExists(cursor, "email_verified") and not cls._ColumnExists(cursor, "active"):
            cursor.execute(
                "ALTER TABLE users CHANGE email_verified active TINYINT(1) NOT NULL DEFAULT 0"
            )

        for column, definition in (
            ("username", "VARCHAR(64) NULL"),
            ("email", "VARCHAR(255) NULL"),
            ("password", "VARCHAR(255) NULL"),
            ("active", "TINYINT(1) NOT NULL DEFAULT 0"),
            ("updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        ):
            if not cls._ColumnExists(cursor, column):
                cursor.execute(f"ALTER TABLE users ADD COLUMN {column} {definition}")

        for column in ("external_id", "display_name", "last_seen_at"):
            if cls._ColumnExists(cursor, column):
                cursor.execute(f"ALTER TABLE users DROP COLUMN {column}")

    @classmethod
    def _ColumnExists(cls, cursor, name: str) -> bool:
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM information_schema.columns
            WHERE table_schema = DATABASE()
              AND table_name = 'users'
              AND column_name = %s
            """,
            (name,),
        )
        row = cursor.fetchone()
        return bool(row and row[0])

    @classmethod
    def _Serialize(cls, row: dict) -> dict:
        return {
            "id": row["id"],
            "username": row.get("username") or "",
            "email": row.get("email") or "",
            "active": bool(row.get("active")),
            "created_at": str(row.get("created_at") or ""),
            "updated_at": str(row.get("updated_at") or ""),
        }

    @classmethod
    def _SerializeDashboard(cls, row: dict) -> dict:
        stored_password = row.get("password") or ""

        return {
            "id": row["id"],
            "username": row.get("username") or "",
            "email": row.get("email") or "",
            "password_preview": Passwords.Preview(stored_password),
            "active": bool(row.get("active")),
            "created_at": str(row.get("created_at") or ""),
        }
