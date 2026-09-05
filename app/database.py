import sqlite3


DATABASE_NAME = "budgetwise.db"


# ==============================
# CREATE DATABASE CONNECTION
# ==============================

def create_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection


# ==============================
# CREATE TABLES
# ==============================

def create_tables():

    connection = create_connection()
    cursor = connection.cursor()

    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            income REAL NOT NULL
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
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()


# ==============================
# CREATE USER
# ==============================

def create_user(name, income):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users (name, income)
        VALUES (?, ?)
    """, (name, income))

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


# ==============================
# GET USER
# ==============================

def get_user(user_id):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, income
        FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()

    connection.close()

    return user


# ==============================
# ADD EXPENSE
# ==============================

def add_expense(user_id, amount, category, description):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses (
            user_id,
            amount,
            category,
            description
        )
        VALUES (?, ?, ?, ?)
    """, (user_id, amount, category, description))

    connection.commit()

    connection.close()


# ==============================
# GET EXPENSES
# ==============================

def get_expenses(user_id):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, amount, category, description
        FROM expenses
        WHERE user_id = ?
    """, (user_id,))

    expenses = cursor.fetchall()

    connection.close()

    return expenses


# ==============================
# UPDATE EXPENSE
# ==============================

def update_expense(
    user_id,
    expense_id,
    amount,
    category,
    description
):

    connection = create_connection()
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

    connection.close()

    return updated


# ==============================
# DELETE EXPENSE
# ==============================

def delete_expense(user_id, expense_id):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
        AND user_id = ?
    """, (expense_id, user_id))

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    return deleted