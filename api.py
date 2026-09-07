from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app import database
from app.auth import hash_password

app = FastAPI(
    title="BudgetWise API",
    description="Personal finance management API",
    version="1.0.0"
)


# ==============================
# PYDANTIC REQUEST MODELS
# ==============================

class Expense(BaseModel):
    user_id: int = Field(gt=0)
    amount: float = Field(gt=0)
    category: str = Field(min_length=2, max_length=50)
    description: str = Field(min_length=2, max_length=200)


class User(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    income: float = Field(gt=0)
    password: str = Field(min_length=8, max_length=100)


# ==============================
# PYDANTIC RESPONSE MODELS
# ==============================

class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: str


class UserCreatedResponse(BaseModel):
    id: int
    name: str
    income: float


class UserResponse(BaseModel):
    id: int
    name: str
    income: float
    total_expenses: float
    balance: float
    expenses: list[ExpenseResponse]


class HighestSpendingCategory(BaseModel):
    category: str | None
    amount: float


class DashboardResponse(BaseModel):
    user: UserCreatedResponse
    income: float
    total_expenses: float
    balance: float
    savings_rate: float
    spending_by_category: dict[str, float]
    highest_spending_category: HighestSpendingCategory
    warning: str


# ==============================
# HOME
# ==============================

@app.get("/")
def home():
    return {
        "message": "Welcome to BudgetWise API",
        "status": "running"
    }


# ==============================
# HEALTH CHECK
# ==============================

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# ==============================
# GET EXPENSES
# ==============================

@app.get(
    "/expenses",
    response_model=dict
)
def get_expenses(user_id: int):

    expenses = database.get_expenses(user_id)

    formatted_expenses = []

    for expense in expenses:
        formatted_expenses.append({
            "id": expense[0],
            "amount": expense[1],
            "category": expense[2],
            "description": expense[3]
        })

    return {
        "user_id": user_id,
        "expenses": formatted_expenses
    }


# ==============================
# CREATE EXPENSE
# ==============================

@app.post("/expenses", response_model=Expense)
def create_expense(expense: Expense):

    database.add_expense(
        expense.user_id,
        expense.amount,
        expense.category,
        expense.description
    )

    return expense


# ==============================
# UPDATE EXPENSE
# ==============================

@app.put(
    "/expenses/{expense_id}",
    response_model=dict
)
def update_expense(
    expense_id: int,
    expense: Expense
):

    updated = database.update_expense(
        expense.user_id,
        expense_id,
        expense.amount,
        expense.category,
        expense.description
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "message": "Expense updated successfully",
        "expense_id": expense_id
    }


# ==============================
# DELETE EXPENSE
# ==============================

@app.delete(
    "/expenses/{expense_id}",
    response_model=dict
)
def delete_expense(
    expense_id: int,
    user_id: int
):

    deleted = database.delete_expense(
        user_id,
        expense_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "message": "Expense deleted successfully",
        "expense_id": expense_id
    }


# ==============================
# CREATE USER
# ==============================

@app.post(
    "/users",
    response_model=UserCreatedResponse
)
def create_user(user: User):

    hashed_password = hash_password(user.password)

    user_id = database.create_user(
        user.name,
        user.income,
        hashed_password
    )

    return {
        "id": user_id,
        "name": user.name,
        "income": user.income
    }


# ==============================
# USER FINANCIAL SUMMARY
# ==============================

@app.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def get_user(user_id: int):

    user = database.get_user(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    expenses = database.get_expenses(user_id)

    formatted_expenses = []

    for expense in expenses:
        formatted_expenses.append({
            "id": expense[0],
            "amount": expense[1],
            "category": expense[2],
            "description": expense[3]
        })

    total_expenses = sum(
        expense[1] for expense in expenses
    )

    balance = user[2] - total_expenses

    return {
        "id": user[0],
        "name": user[1],
        "income": user[2],
        "total_expenses": total_expenses,
        "balance": balance,
        "expenses": formatted_expenses
    }


# ==============================
# FINANCIAL DASHBOARD
# ==============================

@app.get(
    "/users/{user_id}/dashboard",
    response_model=DashboardResponse
)
def financial_dashboard(user_id: int):

    user = database.get_user(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    income = user[2]

    expenses = database.get_expenses(user_id)

    total_expenses = sum(
        expense[1] for expense in expenses
    )

    balance = income - total_expenses

    if income > 0:
        savings_rate = (balance / income) * 100
    else:
        savings_rate = 0

    category_totals = {}

    for expense in expenses:

        category = expense[2]
        amount = expense[1]

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += amount

    if category_totals:

        highest_category = max(
            category_totals,
            key=category_totals.get
        )

        highest_amount = category_totals[highest_category]

    else:

        highest_category = None
        highest_amount = 0

    if total_expenses > income:

        warning = "You have spent more than your income."

    elif total_expenses >= income * 0.8:

        warning = "Warning: You have spent 80% or more of your income."

    elif total_expenses >= income * 0.5:

        warning = "You have spent more than 50% of your income."

    else:

        warning = "Your spending is currently under control."

    return {
        "user": {
            "id": user[0],
            "name": user[1],
            "income": user[2]
        },
        "income": income,
        "total_expenses": total_expenses,
        "balance": balance,
        "savings_rate": round(savings_rate, 2),
        "spending_by_category": category_totals,
        "highest_spending_category": {
            "category": highest_category,
            "amount": highest_amount
        },
        "warning": warning
    }