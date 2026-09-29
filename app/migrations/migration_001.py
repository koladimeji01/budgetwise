import sqlite3

from app.logging_config import logger


# ==========================================
# MIGRATION INFORMATION
# ==========================================

VERSION = 1

DESCRIPTION = "Add expense category index"


# ==========================================
# APPLY MIGRATION
# ==========================================

def upgrade(connection):

    try:

        cursor = connection.cursor()

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_expenses_category
            ON expenses(category)
        """)

        logger.info(
            "Migration 001 applied successfully"
        )

    except sqlite3.Error as error:

        logger.error(
            f"Migration 001 failed: {error}"
        )

        raise
