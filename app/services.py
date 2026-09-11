from app import database


# ==========================================
# GET USER PROFILE
# ==========================================

def get_user_profile(user_id):

    user = database.get_user(user_id)

    if not user:
        return None

    expenses = database.get_expenses(user_id)

    total_expenses = sum(
        expense[1]
        for expense in expenses
    )

    balance = user[2] - total_expenses

    formatted_expenses = []

    for expense in expenses:

        formatted_expenses.append({
            "id": expense[0],
            "amount": expense[1],
            "category": expense[2],
            "description": expense[3]
        })

    return {
        "id": user[0],
        "name": user[1],
        "income": user[2],
        "total_expenses": total_expenses,
        "balance": balance,
        "expenses": formatted_expenses
    }


# ==========================================
# GET USER EXPENSES
# ==========================================

def get_user_expenses(user_id):

    expenses = database.get_expenses(user_id)

    formatted_expenses = []

    for expense in expenses:

        formatted_expenses.append({
            "id": expense[0],
            "amount": expense[1],
            "category": expense[2],
            "description": expense[3]
        })

    return formatted_expenses


# ==========================================
# CREATE EXPENSE
# ==========================================

def create_user_expense(
    user_id,
    amount,
    category,
    description
):

    expense_id = database.add_expense(
        user_id,
        amount,
        category,
        description
    )

    return {
        "id": expense_id,
        "amount": amount,
        "category": category,
        "description": description
    }


# ==========================================
# UPDATE EXPENSE
# ==========================================

def update_user_expense(
    user_id,
    expense_id,
    amount,
    category,
    description
):

    updated = database.update_expense(
        user_id,
        expense_id,
        amount,
        category,
        description
    )

    if not updated:
        return None

    return {
        "id": expense_id,
        "amount": amount,
        "category": category,
        "description": description
    }


# ==========================================
# DELETE EXPENSE
# ==========================================

def delete_user_expense(
    user_id,
    expense_id
):

    deleted = database.delete_expense(
        user_id,
        expense_id
    )

    return deleted > 0


# ==========================================
# GET FINANCIAL DASHBOARD
# ==========================================

def get_user_dashboard(user_id):

    user = database.get_user(user_id)

    if not user:
        return None

    expenses = database.get_expenses(user_id)

    # --------------------------------------
    # TOTAL EXPENSES
    # --------------------------------------

    total_expenses = sum(
        expense[1]
        for expense in expenses
    )

    # --------------------------------------
    # BALANCE
    # --------------------------------------

    balance = user[2] - total_expenses

    # --------------------------------------
    # SPENDING BY CATEGORY
    # --------------------------------------

    spending_by_category = {}

    for expense in expenses:

        category = expense[2]
        amount = expense[1]

        if category not in spending_by_category:
            spending_by_category[category] = 0

        spending_by_category[category] += amount

    # --------------------------------------
    # HIGHEST SPENDING CATEGORY
    # --------------------------------------

    if spending_by_category:

        highest_category = max(
            spending_by_category,
            key=spending_by_category.get
        )

        highest_amount = spending_by_category[
            highest_category
        ]

    else:

        highest_category = None
        highest_amount = 0

    # --------------------------------------
    # SAVINGS RATE
    # --------------------------------------

    if user[2] > 0:

        savings_rate = (
            balance / user[2]
        ) * 100

    else:

        savings_rate = 0

    # --------------------------------------
    # SPENDING WARNING
    # --------------------------------------

    if total_expenses > user[2]:

        warning = (
            "⚠️ You have spent more than your income."
        )

    elif total_expenses >= user[2] * 0.8:

        warning = (
            "⚠️ You have used 80% or more of your income."
        )

    else:

        warning = (
            "✅ Your spending is within a healthy range."
        )

    # --------------------------------------
    # RETURN DASHBOARD
    # --------------------------------------

    return {
        "user": {
            "id": user[0],
            "name": user[1],
            "income": user[2]
        },

        "income": user[2],

        "total_expenses": total_expenses,

        "balance": balance,

        "savings_rate": savings_rate,

        "spending_by_category": spending_by_category,

        "highest_spending_category": {
            "category": highest_category,
            "amount": highest_amount
        },

        "warning": warning
    }
