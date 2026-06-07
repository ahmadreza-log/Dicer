from database.Engine import Engine
from logger.Logger import Logger


class Repository:
    # Persists reusable campaign templates per client owner id.

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
                    owner_id VARCHAR(64) NOT NULL,
                    name VARCHAR(128) NOT NULL,
                    capacity INT NOT NULL DEFAULT 6,
                    is_private TINYINT(1) NOT NULL DEFAULT 0,
                    password VARCHAR(255) NOT NULL DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_campaigns_owner (owner_id)
                )
                """
            )
            Engine.driver.link.commit()
            cursor.close()
            return True, ""
        except Exception as error:
            cls.logger.error("Campaign schema failed | reason=%s", error)
            return False, f"Database error: {error}"

    @classmethod
    def ListByOwner(cls, owner_id: str) -> tuple[bool, str, list[dict]]:
        ready, reason = cls.Ensure()

        if not ready:
            return False, reason, []

        try:
            cursor = Engine.driver.link.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id, owner_id, name, capacity, is_private, password, created_at
                FROM campaigns
                WHERE owner_id = %s
                ORDER BY created_at DESC
                """,
                (owner_id,),
            )
            rows = cursor.fetchall()
            cursor.close()
            items = [cls._Serialize(row) for row in rows]
            return True, "", items
        except Exception as error:
            cls.logger.error("Campaign list failed | owner=%s | reason=%s", owner_id, error)
            return False, f"Database error: {error}", []

    @classmethod
    def Save(
        cls,
        owner_id: str,
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
                INSERT INTO campaigns (owner_id, name, capacity, is_private, password)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (owner_id, name, capacity, int(is_private), password),
            )
            campaign_id = cursor.lastrowid
            Engine.driver.link.commit()
            cursor.close()
            campaign = cls.Get(campaign_id, owner_id)

            cls.logger.info(
                "Campaign saved | id=%s | owner=%s | name=%s",
                campaign_id,
                owner_id,
                name,
            )
            return True, "", campaign
        except Exception as error:
            cls.logger.error("Campaign save failed | owner=%s | reason=%s", owner_id, error)
            return False, f"Database error: {error}", None

    @classmethod
    def Get(cls, campaign_id: int, owner_id: str) -> dict | None:
        if not Engine.IsActive():
            return None

        try:
            cursor = Engine.driver.link.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id, owner_id, name, capacity, is_private, password, created_at
                FROM campaigns
                WHERE id = %s AND owner_id = %s
                LIMIT 1
                """,
                (campaign_id, owner_id),
            )
            row = cursor.fetchone()
            cursor.close()

            if row is None:
                return None

            return cls._Serialize(row)
        except Exception as error:
            cls.logger.error(
                "Campaign fetch failed | id=%s | owner=%s | reason=%s",
                campaign_id,
                owner_id,
                error,
            )
            return None

    @classmethod
    def _Serialize(cls, row: dict) -> dict:
        return {
            "id": row["id"],
            "owner_id": row["owner_id"],
            "name": row["name"],
            "capacity": row["capacity"],
            "private": bool(row["is_private"]),
            "password": row["password"],
            "created_at": str(row["created_at"]),
        }
