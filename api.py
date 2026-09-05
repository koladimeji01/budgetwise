from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app import database


app = FastAPI(
    title="BudgetWise API",
    description="Personal finance management API",
    version="1.0.0"
)


# ==============================
# PYDANTIC MODELS
# ==============================

class Expense(BaseModel):
    user_id: int = Field(gt=0)
    amount: float = Field(gt=0)
    category: str = Field(min_length=2, max_length=50)
    description: str = Field(min_length=2, max_length=200)


class User(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    income: float = Field(gt=0)


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

@app.get("/expenses")
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

@app.post("/expenses")
def create_expense(expense: Expense):

    database.add_expense(
        expense.user_id,
        expense.amount,
        expense.category,
        expense.description
    )

    return {
        "message": "Expense saved successfully",
        "expense": expense
    }


# ==============================
# UPDATE EXPENSE
# ==============================

@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: Expense):

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

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, user_id: int):

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

@app.post("/users")
def create_user(user: User):

    user_id = database.create_user(
        user.name,
        user.income
    )

    return {
        "message": "User created successfully",
        "user": {
            "id": user_id,
            "name": user.name,
            "income": user.income
        }
    }