from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import sqlite3

from app import database
from app import services

from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="BudgetWise API",
    description="Personal finance management API",
    version="1.0.0"
)


# ==========================================
# SECURITY
# ==========================================

security = HTTPBearer()


# ==========================================
# DATABASE ERROR HANDLER
# ==========================================

@app.exception_handler(sqlite3.Error)
async def database_exception_handler(request, exc):

    return JSONResponse(
        status_code=500,
        content={
            "detail": "A database error occurred. Please try again later."
        }
    )


# ==========================================
# REQUEST MODELS
# ==========================================

class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)

    category: str = Field(
        min_length=2,
        max_length=50
    )

    description: str = Field(
        min_length=2,
        max_length=200
    )


class User(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50
    )

    income: float = Field(gt=0)

    password: str = Field(
        min_length=8,
        max_length=100
    )


class LoginRequest(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50
    )

    password: str = Field(
        min_length=8,
        max_length=100
    )


# ==========================================
# RESPONSE MODELS
# ==========================================

class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: str


class ExpenseListResponse(BaseModel):
    user_id: int
    expenses: list[ExpenseResponse]


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


# ==========================================
# GET CURRENT USER
# ==========================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = decode_access_token(token)

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user_id = payload.get("user_id")

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = database.get_user(user_id)

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Welcome to BudgetWise API"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# ==========================================
# CREATE USER
# ==========================================

@app.post(
    "/users",
    response_model=UserCreatedResponse
)
def create_user(user: User):

    existing_user = database.get_user_by_name(
        user.name
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(
        user.password
    )

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


# ==========================================
# LOGIN
# ==========================================

@app.post("/login")
def login(login_data: LoginRequest):

    user = database.get_user_by_name(
        login_data.name
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    password_is_correct = verify_password(
        login_data.password,
        user[3]
    )

    if not password_is_correct:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        user[0]
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==========================================
# GET MY PROFILE
# ==========================================

@app.get(
    "/users/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user=Depends(get_current_user)
):

    user_id = current_user[0]

    profile = services.get_user_profile(user_id)

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return profile


# ==========================================
# GET MY EXPENSES
# ==========================================

@app.get(
    "/expenses",
    response_model=ExpenseListResponse
)
def get_expenses(
    current_user=Depends(get_current_user)
):

    user_id = current_user[0]

    expenses = services.get_user_expenses(user_id)

    return {
        "user_id": user_id,
        "expenses": expenses
    }


# ==========================================
# CREATE EXPENSE
# ==========================================

@app.post(
    "/expenses",
    response_model=ExpenseResponse
)
def create_expense(
    expense: ExpenseCreate,
    current_user=Depends(get_current_user)
):

    user_id = current_user[0]

    new_expense = services.create_user_expense(
        user_id,
        expense.amount,
        expense.category,
        expense.description
    )

    return new_expense


# ==========================================
# UPDATE EXPENSE
# ==========================================

@app.put(
    "/expenses/{expense_id}",
    response_model=ExpenseResponse
)
def update_expense(
    expense_id: int,
    expense: ExpenseCreate,
    current_user=Depends(get_current_user)
):

    user_id = current_user[0]

    updated_expense = services.update_user_expense(
        user_id,
        expense_id,
        expense.amount,
        expense.category,
        expense.description
    )

    if not updated_expense:

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return updated_expense


# ==========================================
# DELETE EXPENSE
# ==========================================

@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    current_user=Depends(get_current_user)
):

    user_id = current_user[0]

    deleted = services.delete_user_expense(
        user_id,
        expense_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "message": "Expense deleted successfully"
    }


# ==========================================
# FINANCIAL DASHBOARD
# ==========================================

@app.get(
    "/users/me/dashboard",
    response_model=DashboardResponse
)
def get_dashboard(
    current_user=Depends(get_current_user)
):

    user_id = current_user[0]

    dashboard = services.get_user_dashboard(
        user_id
    )

    if not dashboard:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return dashboard