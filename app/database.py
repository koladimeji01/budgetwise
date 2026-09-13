import sqlite3

from app.config import DATABASE_NAME


# ==========================================
# DATABASE CONNECTION
# ==========================================

def create_connection():
    try:
        connection = sqlite3.connect(DATABASE_NAME)

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection

    except sqlite3.Error as error:
        print(
            f"Database connection error: {error}"
        )
        raise
    
# ==========================================
# CREATE TABLES
# ==========================================

def create_tables():
    connection = create_connection()

    try:
        cursor = connection.cursor()

        # USERS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                income REAL NOT NULL,
                password TEXT NOT NULL
            )
        """)

        # EXPENSES TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,

                FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
            )
        """)

        connection.commit()

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Database error while creating tables: {error}")
        raise

    finally:
        connection.close()


# ==========================================
# CREATE USER
# ==========================================

def create_user(name, income, password):
    connection = create_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (
                name,
                income,
                password
            )
            VALUES (?, ?, ?)
        """, (
            name,
            income,
            password
        ))

        connection.commit()

        user_id = cursor.lastrowid

        return user_id

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Database error while creating user: {error}")
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
                income
            FROM users
            WHERE id = ?
        """, (user_id,))

        user = cursor.fetchone()

        return user

    except sqlite3.Error as error:
        print(f"Database error while getting user: {error}")
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
                password
            FROM users
            WHERE name = ?
        """, (name,))

        user = cursor.fetchone()

        return user

    except sqlite3.Error as error:
        print(f"Database error while getting user by name: {error}")
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

        expense_id = cursor.lastrowid

        return expense_id

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Database error while adding expense: {error}")
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

        expenses = cursor.fetchall()

        return expenses

    except sqlite3.Error as error:
        print(f"Database error while getting expenses: {error}")
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

        updated = cursor.rowcount

        return updated

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Database error while updating expense: {error}")
        raise

    finally:
        connection.close()


# ==========================================
# DELETE EXPENSE
# ==========================================

def delete_expense(user_id, expense_id):
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

        deleted = cursor.rowcount

        return deleted

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Database error while deleting expense: {error}")
        raise

    finally:
        connection.close()