print("==============================")
print("       BUDGETWISE")
print("==============================")

print()


# INPUT VALIDATION

def get_valid_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return amount

        except ValueError:
            print("Invalid amount. Please enter a number.")


def get_valid_text(prompt):
    while True:
        value = input(prompt).strip()

        if value == "":
            print("This field cannot be empty.")
            continue

        return value


# USER INFORMATION

name = get_valid_text("What is your name? ")

print()
print(f"Welcome, {name}!")
print("Let's help you manage your money.")

income = get_valid_amount(
    "What is your monthly income? ₦"
)

print()
print(f"Your monthly income is ₦{income:,.2f}")


# STORE EXPENSES


expenses = []

# ADD EXPENSE

def add_expense():

    amount = get_valid_amount(
        "Enter expense amount: ₦"
    )

    category = get_valid_text(
        "Enter category: "
    )

    description = get_valid_text(
        "Enter description: "
    )

    expense = {
        "amount": amount,
        "category": category,
        "description": description
    }

    expenses.append(expense)

    print("Expense added successfully!")


# VIEW EXPENSES

def view_expenses():

    print("\n--------- EXPENSES ---------")

    if len(expenses) == 0:
        print("No expenses recorded.")
        return

    for expense in expenses:

        print(f"Category: {expense['category']}")
        print(f"Amount: ₦{expense['amount']:,.2f}")
        print(f"Description: {expense['description']}")
        print("---------------------------")


# CALCULATE TOTAL EXPENSES

def total_expenses():

    total = 0

    for expense in expenses:
        total += expense["amount"]

    return total



# SHOW BALANCE

def show_balance(income):

    total = total_expenses()

    balance = income - total

    print(f"\nTotal income: ₦{income:,.2f}")
    print(f"Total expenses: ₦{total:,.2f}")
    print(f"Remaining balance: ₦{balance:,.2f}")


# MAIN MENU

while True:

    print("\n--------- MENU ---------")

    print("1. Add Expense")
    print("2. View Expenses")
    print("3. View Total Expenses")
    print("4. View Balance")
    print("5. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":

        add_expense()

    elif choice == "2":

        view_expenses()

    elif choice == "3":

        print(
            f"Total expenses: "
            f"₦{total_expenses():,.2f}"
        )

    elif choice == "4":

        show_balance(income)

    elif choice == "5":

        print("Thank you for using BudgetWise!")

        break

    else:

        print(
            "Invalid option. "
            "Please choose a number from 1 to 5."
        )