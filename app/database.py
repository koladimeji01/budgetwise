import sqlite3

from app.config import DATABASE_NAME
from app.logging_config import logger


# ==========================================
# CREATE DATABASE CONNECTION
# ==========================================

def create_connection():

    try:

        connection = sqlite3.connect(
            DATABASE_NAME
        )

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection

    except sqlite3.Error as error:

        logger.error(
            f"Database connection error: {error}"
        )

        raise


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

def create_tables():

    connection = create_connection()

    try:

        cursor = connection.cursor()

        # ----------------------------------
        # USERS TABLE
        # ----------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                income REAL NOT NULL CHECK(income > 0),
                password TEXT NOT NULL,
                email TEXT
            )
        """)

        # ----------------------------------
        # EXPENSES TABLE
        # ----------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                description TEXT NOT NULL,

                FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
            )
        """)

        # ----------------------------------
        # EXPENSE INDEX
        # ----------------------------------

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_expenses_user_id
            ON expenses(user_id)
        """)

        # ----------------------------------
        # EMAIL UNIQUE INDEX
        # ----------------------------------

        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_users_email
            ON users(email)
            WHERE email IS NOT NULL
        """)

        connection.commit()

        logger.info(
            "Database tables created successfully"
        )

    except sqlite3.Error as error:

        connection.rollback()

        logger.error(
            f"Database error while creating tables: {error}"
        )

        raise

    finally:

        connection.close()


# ==========================================
# CREATE USER
# ==========================================

def create_user(
    name,
    income,
    password,
    email
):

    connection = create_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (
                name,
                income,
                password,
                email
            )
            VALUES (?, ?, ?, ?)
        """, (
            name,
            income,
            password,
            email
        ))

        connection.commit()

        user_id = cursor.lastrowid

        return user_id

    except sqlite3.Error as error:

        connection.rollback()

        logger.error(
            f"Database error while creating user: {error}"
        )

        raise

    finally:

        connection.close()


# ==========================================
# GET USER BY ID
# ==========================================

def get_user(user_id):

    connection = create_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                income,
                email
            FROM users
            WHERE id = ?
        """, (user_id,))

        return cursor.fetchone()

    except sqlite3.Error as error:

        logger.error(
            f"Database error while getting user: {error}"
        )

        raise

    finally:

        connection.close()


# ==========================================
# GET USER BY NAME
# ==========================================

def get_user_by_name(name):

    connection = create_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                income,
                password,
                email
            FROM users
            WHERE name = ?
            LIMIT 1
        """, (name,))

        return cursor.fetchone()

    except sqlite3.Error as error:

        logger.error(
            f"Database error while getting user by name: {error}"
        )

        raise

    finally:

        connection.close()


# ==========================================
# GET USER BY EMAIL
# ==========================================

def get_user_by_email(email):

    connection = create_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                income,
                password,
                email
            FROM users
            WHERE email = ?
            LIMIT 1
        """, (email,))

        return cursor.fetchone()

    except sqlite3.Error as error:

        logger.error(
            f"Database error while getting user by email: {error}"
        )

        raise

    finally:

        connection.close()


# ==========================================
# ADD EXPENSE
# ==========================================

def add_expense(
    user_id,
    amount,
    category,
    description
):

    connection = create_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO expenses (
                user_id,
                amount,
                category,
                description
            )
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            amount,
            category,
            description
        ))

        connection.commit()

        return cursor.lastrowid

    except sqlite3.Error as error:

        connection.rollback()

        logger.error(
            f"Database error while adding expense: {error}"
        )

        raise

    finally:

        connection.close()


# ==========================================
# GET USER EXPENSES
# ==========================================

def get_expenses(user_id):

    connection = create_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                amount,
                category,
                description
            FROM expenses
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,))

        return cursor.fetchall()

    except sqlite3.Error as error:

        logger.error(
            f"Database error while getting expenses: {error}"
        )

        raise

    finally:

        connection.close()


# ==========================================
# UPDATE EXPENSE
# ==========================================

def update_expense(
    user_id,
    expense_id,
    amount,
    category,
    description
):

    connection = create_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE expenses
            SET
                amount = ?,
                category = ?,
                description = ?
            WHERE
                id = ?
                AND user_id = ?
        """, (
            amount,
            category,
            description,
            expense_id,
            user_id
        ))

        connection.commit()

        return cursor.rowcount

    except sqlite3.Error as error:

        connection.rollback()

        logger.error(
            f"Database error while updating expense: {error}"
        )

        raise

    finally:

        connection.close()


# ==========================================
# DELETE EXPENSE
# ==========================================

def delete_expense(
    user_id,
    expense_id
):

    connection = create_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM expenses
            WHERE
                id = ?
                AND user_id = ?
        """, (
            expense_id,
            user_id
        ))

        connection.commit()

        return cursor.rowcount

    except sqlite3.Error as error:

        connection.rollback()

        logger.error(
            f"Database error while deleting expense: {error}"
        )

        raise

    finally:

        connection.close()