from database.Engine import Engine
from logger.Logger import Logger


class Repository:
    # Persists room templates (campaigns) owned by a registered user.

    logger = Logger.Get("Campaigns")

    @classmethod
    def Ensure(cls) -> tuple[bool, str]:
        if not Engine.IsActive():
            return False, "Database is not connected."

        try:
            cursor = Engine.driver.link.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS campaigns (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    name VARCHAR(128) NOT NULL,
                    capacity INT NOT NULL DEFAULT 6,
                    is_private TINYINT(1) NOT NULL DEFAULT 0,
                    password VARCHAR(255) NOT NULL DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_campaigns_user (user_id)
                )
                """
            )
            cls._MigrateSchema(cursor)
            Engine.driver.link.commit()
            cursor.close()
            return True, ""
        except Exception as error:
            cls.logger.error("Campaign schema failed | reason=%s", error)
            return False, f"Database error: {error}"

    @classmethod
    def ListByUser(cls, user_id: int) -> tuple[bool, str, list[dict]]:
        ready, reason = cls.Ensure()

        if not ready:
            return False, reason, []

        try:
            cursor = Engine.driver.link.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id, user_id, name, capacity, is_private, password, created_at
                FROM campaigns
                WHERE user_id = %s
                ORDER BY created_at DESC
                """,
                (user_id,),
            )
            rows = cursor.fetchall()
            cursor.close()
            items = [cls._Serialize(row) for row in rows]
            return True, "", items
        except Exception as error:
            cls.logger.error("Campaign list failed | user_id=%s | reason=%s", user_id, error)
            return False, f"Database error: {error}", []

    @classmethod
    def Save(
        cls,
        user_id: int,
        name: str,
        capacity: int,
        is_private: bool,
        password: str,
    ) -> tuple[bool, str, dict | None]:
        ready, reason = cls.Ensure()

        if not ready:
            return False, reason, None

        try:
            cursor = Engine.driver.link.cursor()
            cursor.execute(
                """
                INSERT INTO campaigns (user_id, name, capacity, is_private, password)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (user_id, name, capacity, int(is_private), password),
            )
            campaign_id = cursor.lastrowid
            Engine.driver.link.commit()
            cursor.close()
            campaign = cls.Get(campaign_id, user_id)

            cls.logger.info(
                "Campaign saved | id=%s | user_id=%s | name=%s",
                campaign_id,
                user_id,
                name,
            )
            return True, "", campaign
        except Exception as error:
            cls.logger.error("Campaign save failed | user_id=%s | reason=%s", user_id, error)
            return False, f"Database error: {error}", None

    @classmethod
    def Get(cls, campaign_id: int, user_id: int) -> dict | None:
        if not Engine.IsActive():
            return None

        try:
            cursor = Engine.driver.link.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id, user_id, name, capacity, is_private, password, created_at
                FROM campaigns
                WHERE id = %s AND user_id = %s
                LIMIT 1
                """,
                (campaign_id, user_id),
            )
            row = cursor.fetchone()
            cursor.close()

            if row is None:
                return None

            return cls._Serialize(row)
        except Exception as error:
            cls.logger.error(
                "Campaign fetch failed | id=%s | user_id=%s | reason=%s",
                campaign_id,
                user_id,
                error,
            )
            return None

    @classmethod
    def _MigrateSchema(cls, cursor) -> None:
        if cls._ColumnExists(cursor, "owner_id") and not cls._ColumnExists(cursor, "user_id"):
            cursor.execute("ALTER TABLE campaigns ADD COLUMN user_id INT NOT NULL DEFAULT 0")
            cursor.execute("ALTER TABLE campaigns DROP COLUMN owner_id")

        if not cls._ColumnExists(cursor, "user_id"):
            cursor.execute("ALTER TABLE campaigns ADD COLUMN user_id INT NOT NULL DEFAULT 0")

    @classmethod
    def _ColumnExists(cls, cursor, name: str) -> bool:
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM information_schema.columns
            WHERE table_schema = DATABASE()
              AND table_name = 'campaigns'
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
            "user_id": row["user_id"],
            "name": row["name"],
            "capacity": row["capacity"],
            "private": bool(row["is_private"]),
            "password": row["password"],
            "created_at": str(row["created_at"]),
        }
