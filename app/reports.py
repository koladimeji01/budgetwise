from app import database


# ==========================================
# TOTAL EXPENSES
# ==========================================

def total_expenses(user_id):

    expenses = database.get_expenses(
        user_id
    )

    total = 0

    for expense in expenses:

        total += expense[1]

    return total


# ==========================================
# SPENDING BY CATEGORY
# ==========================================

def spending_by_category(user_id):

    expenses = database.get_expenses(
        user_id
    )

    categories = {}

    for expense in expenses:

        category = expense[2]
        amount = expense[1]

        if category in categories:

            categories[category] += amount

        else:

            categories[category] = amount

    return categories


# ==========================================
# CATEGORY SUMMARY
# ==========================================

def show_category_summary(user_id):

    categories = spending_by_category(
        user_id
    )

    print(
        "\n--------- SPENDING BY CATEGORY ---------"
    )

    if not categories:

        print(
            "No expenses recorded."
        )

        return

    for category, amount in categories.items():

        print(
            f"{category}: ₦{amount:,.2f}"
        )


# ==========================================
# HIGHEST SPENDING
# ==========================================

def highest_spending_category(user_id):

    categories = spending_by_category(
        user_id
    )

    if not categories:

        print(
            "No expenses recorded."
        )

        return

    highest_category = max(
        categories,
        key=categories.get
    )

    highest_amount = categories[
        highest_category
    ]

    print(
        "\n--------- HIGHEST SPENDING ---------"
    )

    print(
        f"Category: {highest_category}"
    )

    print(
        f"Amount: ₦{highest_amount:,.2f}"
    )


# ==========================================
# SAVINGS RATE
# ==========================================

def savings_rate(user_id, income):

    total = total_expenses(user_id)

    savings = income - total

    if income <= 0:

        return 0

    return (
        savings / income
    ) * 100


# ==========================================
# BALANCE
# ==========================================

def show_balance(user_id, income):

    total = total_expenses(user_id)

    balance = income - total

    print(
        "\n--------- BALANCE ---------"
    )

    print(
        f"Total income: ₦{income:,.2f}"
    )

    print(
        f"Total expenses: ₦{total:,.2f}"
    )

    print(
        f"Remaining balance: ₦{balance:,.2f}"
    )


# ==========================================
# SPENDING WARNING
# ==========================================

def spending_warning(user_id, income):

    total = total_expenses(user_id)

    if income <= 0:

        return

    percentage = (
        total / income
    ) * 100

    print(
        "\n--------- SPENDING STATUS ---------"
    )

    print(
        f"You have spent "
        f"{percentage:.2f}% "
        f"of your income."
    )

    if percentage >= 90:

        print(
            "🚨 WARNING: You have spent "
            "90% or more of your income."
        )

    elif percentage >= 70:

        print(
            "⚠️ CAUTION: Your spending "
            "is getting high."
        )

    elif percentage >= 50:

        print(
            "💡 You have used more than "
            "half of your income."
        )

    else:

        print(
            "✅ Your spending is currently "
            "under control."
        )


# ==========================================
# FINANCIAL DASHBOARD
# ==========================================

def financial_dashboard(user_id, income):

    total = total_expenses(user_id)

    balance = income - total

    rate = savings_rate(
        user_id,
        income
    )

    print()
    print(
        "======================================"
    )

    print(
        "        FINANCIAL DASHBOARD"
    )

    print(
        "======================================"
    )

    print(
        f"Monthly Income:    "
        f"₦{income:,.2f}"
    )

    print(
        f"Total Expenses:    "
        f"₦{total:,.2f}"
    )

    print(
        f"Remaining Balance: "
        f"₦{balance:,.2f}"
    )

    print(
        f"Savings Rate:      "
        f"{rate:.2f}%"
    )

    show_category_summary(user_id)

    highest_spending_category(
        user_id
    )

    spending_warning(
        user_id,
        income
    )

    print(
        "======================================"
    )