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
                    room_id VARCHAR(10) NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_campaigns_user (user_id),
                    UNIQUE KEY uq_campaigns_user_name (user_id, name),
                    UNIQUE KEY uq_campaigns_room_id (room_id)
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
                SELECT id, user_id, name, capacity, is_private, password, room_id, created_at
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

        resolved_name = name.strip()

        if not resolved_name:
            return False, "Campaign name is required.", None

        if cls.GetByName(user_id, resolved_name) is not None:
            return False, "A campaign with this name already exists.", None

        try:
            cursor = Engine.driver.link.cursor()
            cursor.execute(
                """
                INSERT INTO campaigns (user_id, name, capacity, is_private, password)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (user_id, resolved_name, capacity, int(is_private), password),
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
            message = str(error).lower()

            if "duplicate" in message and "name" in message:
                return False, "A campaign with this name already exists.", None

            return False, f"Database error: {error}", None

    @classmethod
    def GetByName(cls, user_id: int, name: str) -> dict | None:
        if not Engine.IsActive():
            return None

        resolved_name = name.strip()

        if not resolved_name:
            return None

        try:
            cursor = Engine.driver.link.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id, user_id, name, capacity, is_private, password, room_id, created_at
                FROM campaigns
                WHERE user_id = %s AND name = %s
                LIMIT 1
                """,
                (user_id, resolved_name),
            )
            row = cursor.fetchone()
            cursor.close()

            if row is None:
                return None

            return cls._Serialize(row)
        except Exception as error:
            cls.logger.error(
                "Campaign fetch failed | user_id=%s | name=%s | reason=%s",
                user_id,
                name,
                error,
            )
            return None

    @classmethod
    def AssignRoom(cls, campaign_id: int, user_id: int, room_id: str) -> tuple[bool, str]:
        ready, reason = cls.Ensure()

        if not ready:
            return False, reason

        resolved_room = room_id.strip()

        if not resolved_room:
            return False, "Room ID is required."

        try:
            cursor = Engine.driver.link.cursor()
            cursor.execute(
                """
                UPDATE campaigns
                SET room_id = %s
                WHERE id = %s AND user_id = %s AND room_id IS NULL
                """,
                (resolved_room, campaign_id, user_id),
            )
            updated = cursor.rowcount
            Engine.driver.link.commit()
            cursor.close()

            if updated == 0:
                existing = cls.Get(campaign_id, user_id)

                if existing and existing.get("room_id"):
                    return False, "This campaign already has a room assigned."

                return False, "Campaign not found."

            cls.logger.info(
                "Campaign room assigned | campaign_id=%s | room_id=%s",
                campaign_id,
                resolved_room,
            )
            return True, ""
        except Exception as error:
            cls.logger.error(
                "Campaign room assign failed | campaign_id=%s | room_id=%s | reason=%s",
                campaign_id,
                room_id,
                error,
            )
            message = str(error).lower()

            if "duplicate" in message and "room_id" in message:
                return False, "Room ID is already assigned to another campaign."

            return False, f"Database error: {error}"

    @classmethod
    def ClearRoom(cls, campaign_id: int) -> None:
        if not Engine.IsActive():
            return

        try:
            cursor = Engine.driver.link.cursor()
            cursor.execute(
                """
                UPDATE campaigns
                SET room_id = NULL
                WHERE id = %s
                """,
                (campaign_id,),
            )
            Engine.driver.link.commit()
            cursor.close()
        except Exception as error:
            cls.logger.error(
                "Campaign room clear failed | campaign_id=%s | reason=%s",
                campaign_id,
                error,
            )

    @classmethod
    def ClearLiveRoomIds(cls) -> None:
        if not Engine.IsActive():
            return

        try:
            cursor = Engine.driver.link.cursor()
            cursor.execute("UPDATE campaigns SET room_id = NULL WHERE room_id IS NOT NULL")
            Engine.driver.link.commit()
            cursor.close()
            cls.logger.info("Cleared live campaign room ids")
        except Exception as error:
            cls.logger.error("Campaign room reset failed | reason=%s", error)

    @classmethod
    def Get(cls, campaign_id: int, user_id: int) -> dict | None:
        if not Engine.IsActive():
            return None

        try:
            cursor = Engine.driver.link.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id, user_id, name, capacity, is_private, password, room_id, created_at
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

        if not cls._IndexExists(cursor, "uq_campaigns_user_name"):
            try:
                cursor.execute(
                    "ALTER TABLE campaigns ADD UNIQUE KEY uq_campaigns_user_name (user_id, name)"
                )
            except Exception as error:
                cls.logger.warning(
                    "Campaign unique name index skipped | reason=%s",
                    error,
                )

        if not cls._ColumnExists(cursor, "room_id"):
            cursor.execute("ALTER TABLE campaigns ADD COLUMN room_id VARCHAR(10) NULL")

        if not cls._IndexExists(cursor, "uq_campaigns_room_id"):
            try:
                cursor.execute(
                    "ALTER TABLE campaigns ADD UNIQUE KEY uq_campaigns_room_id (room_id)"
                )
            except Exception as error:
                cls.logger.warning(
                    "Campaign unique room id index skipped | reason=%s",
                    error,
                )

    @classmethod
    def _IndexExists(cls, cursor, name: str) -> bool:
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM information_schema.statistics
            WHERE table_schema = DATABASE()
              AND table_name = 'campaigns'
              AND index_name = %s
            """,
            (name,),
        )
        row = cursor.fetchone()
        return bool(row and row[0])

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
            "room_id": row.get("room_id") or "",
            "created_at": str(row["created_at"]),
        }
