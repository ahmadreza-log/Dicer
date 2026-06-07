import secrets
import string
from datetime import datetime, timedelta

from database.Engine import Engine
from logger.Logger import Logger


class Repository:
    # Short-lived email verification codes for in-app activation.

    logger = Logger.Get("ActivationCodes")
    CodeLength = 6
    CodeTtlMinutes = 15
    PurposeEmailVerify = "email_verify"
    Alphabet = string.digits

    @classmethod
    def Ensure(cls) -> tuple[bool, str]:
        if not Engine.IsActive():
            return False, "Database is not connected."

        try:
            cursor = Engine.driver.link.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS activation_codes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    code CHAR(6) NOT NULL,
                    purpose VARCHAR(32) NOT NULL DEFAULT 'email_verify',
                    expires_at TIMESTAMP NOT NULL,
                    used_at TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_activation_user (user_id),
                    INDEX idx_activation_code (code),
                    INDEX idx_activation_lookup (user_id, code, purpose),
                    CONSTRAINT fk_activation_user
                        FOREIGN KEY (user_id) REFERENCES users(id)
                        ON DELETE CASCADE
                )
                """
            )
            Engine.driver.link.commit()
            cursor.close()
            return True, ""
        except Exception as error:
            cls.logger.error("Activation code schema failed | reason=%s", error)
            return False, f"Database error: {error}"

    @classmethod
    def Issue(cls, user_id: int, purpose: str = PurposeEmailVerify) -> tuple[bool, str, str]:
        ready, reason = cls.Ensure()

        if not ready:
            return False, reason, ""

        code = cls._GenerateCode()
        expires_at = datetime.utcnow() + timedelta(minutes=cls.CodeTtlMinutes)

        try:
            cursor = Engine.driver.link.cursor()
            cursor.execute(
                """
                UPDATE activation_codes
                SET used_at = CURRENT_TIMESTAMP
                WHERE user_id = %s AND purpose = %s AND used_at IS NULL
                """,
                (user_id, purpose),
            )
            cursor.execute(
                """
                INSERT INTO activation_codes (user_id, code, purpose, expires_at)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, code, purpose, expires_at),
            )
            Engine.driver.link.commit()
            cursor.close()
            cls.logger.info("Activation code issued | user_id=%s | purpose=%s", user_id, purpose)
            return True, "", code
        except Exception as error:
            cls.logger.error(
                "Activation code issue failed | user_id=%s | reason=%s",
                user_id,
                error,
            )
            return False, f"Database error: {error}", ""

    @classmethod
    def Verify(cls, user_id: int, code: str, purpose: str = PurposeEmailVerify) -> tuple[bool, str]:
        ready, reason = cls.Ensure()

        if not ready:
            return False, reason

        normalized = code.strip()

        if len(normalized) != cls.CodeLength or not normalized.isdigit():
            return False, "Invalid verification code."

        try:
            cursor = Engine.driver.link.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id, expires_at, used_at
                FROM activation_codes
                WHERE user_id = %s AND code = %s AND purpose = %s
                ORDER BY id DESC
                LIMIT 1
                """,
                (user_id, normalized, purpose),
            )
            row = cursor.fetchone()

            if row is None:
                cursor.close()
                return False, "Verification code is incorrect."

            if row["used_at"] is not None:
                cursor.close()
                return False, "Verification code has already been used."

            cursor.execute(
                """
                SELECT id
                FROM activation_codes
                WHERE id = %s AND expires_at > UTC_TIMESTAMP()
                """,
                (row["id"],),
            )
            valid_row = cursor.fetchone()

            if valid_row is None:
                cursor.close()
                return False, "Verification code has expired."

            cursor.execute(
                """
                UPDATE activation_codes
                SET used_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (row["id"],),
            )
            Engine.driver.link.commit()
            cursor.close()
            return True, ""
        except Exception as error:
            cls.logger.error(
                "Activation code verify failed | user_id=%s | reason=%s",
                user_id,
                error,
            )
            return False, f"Database error: {error}"

    @classmethod
    def _GenerateCode(cls) -> str:
        return "".join(secrets.choice(cls.Alphabet) for _ in range(cls.CodeLength))
