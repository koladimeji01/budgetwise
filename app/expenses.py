from app import database

from app.utils import (
    get_valid_amount,
    get_valid_text,
    get_valid_id
)


# ==========================================
# ADD EXPENSE
# ==========================================

def add_expense(user_id):

    amount = get_valid_amount(
        "Enter expense amount: ₦"
    )

    category = get_valid_text(
        "Enter category: "
    )

    description = get_valid_text(
        "Enter description: "
    )

    database.add_expense(
        user_id,
        amount,
        category,
        description
    )

    print(
        "✅ Expense added successfully!"
    )


# ==========================================
# VIEW EXPENSES
# ==========================================

def view_expenses(user_id):

    expenses = database.get_expenses(
        user_id
    )

    print(
        "\n--------- EXPENSES ---------"
    )

    if not expenses:

        print(
            "No expenses recorded."
        )

        return

    for expense in expenses:

        print(f"ID: {expense[0]}")
        print(f"Category: {expense[2]}")
        print(f"Amount: ₦{expense[1]:,.2f}")
        print(
            f"Description: {expense[3]}"
        )

        print(
            "---------------------------"
        )


# ==========================================
# UPDATE EXPENSE
# ==========================================

def update_expense(user_id):

    expense_id = get_valid_id(
        "Enter expense ID to update: "
    )

    amount = get_valid_amount(
        "Enter new amount: ₦"
    )

    category = get_valid_text(
        "Enter new category: "
    )

    description = get_valid_text(
        "Enter new description: "
    )

    updated = database.update_expense(
        user_id,
        expense_id,
        amount,
        category,
        description
    )

    if updated:

        print(
            "✅ Expense updated successfully!"
        )

    else:

        print(
            "❌ Expense not found."
        )


# ==========================================
# DELETE EXPENSE
# ==========================================

def delete_expense(user_id):

    expense_id = get_valid_id(
        "Enter expense ID to delete: "
    )

    confirmation = input(
        "Are you sure? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":

        print(
            "Deletion cancelled."
        )

        return

    deleted = database.delete_expense(
        user_id,
        expense_id
    )

    if deleted:

        print(
            "✅ Expense deleted successfully!"
        )

    else:

        print(
            "❌ Expense not found."
        )