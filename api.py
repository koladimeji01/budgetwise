from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from app import database
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
# REQUEST MODELS
# ==========================================

class Expense(BaseModel):
    user_id: int = Field(gt=0)
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
# AUTHENTICATION
# ==========================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get the currently logged-in user
    from the JWT token.
    """

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
# HOME ROUTE
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
# REGISTER USER
# ==========================================

@app.post(
    "/users",
    response_model=UserCreatedResponse
)
def create_user(user: User):

    # Check if username already exists
    existing_user = database.get_user_by_name(
        user.name
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Hash the password before saving
    hashed_password = hash_password(
        user.password
    )

    # Create the user
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

    # Find user
    user = database.get_user_by_name(
        login_data.name
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Check password
    password_is_correct = verify_password(
        login_data.password,
        user[3]
    )

    if not password_is_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Create JWT token
    access_token = create_access_token(
        user[0]
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==========================================
# MY PROFILE
# ==========================================

@app.get("/users/me")
def get_my_profile(
    current_user=Depends(get_current_user)
):

    return {
        "id": current_user[0],
        "name": current_user[1],
        "income": current_user[2]
    }


# ==========================================
# GET USER BY ID
# ==========================================

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

    total = 0

    for expense in expenses:

        total += expense[1]

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
        "total_expenses": total,
        "balance": user[2] - total,
        "expenses": formatted_expenses
    }


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

    # Get logged-in user's ID
    user_id = current_user[0]

    expenses = database.get_expenses(
        user_id
    )

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


# ==========================================
# ADD EXPENSE
# ==========================================

@app.post(
    "/expenses",
    response_model=ExpenseResponse
)
def create_expense(
    expense: Expense,
    current_user=Depends(get_current_user)
):

    # Get logged-in user's ID
    user_id = current_user[0]

    # Make sure user_id from request
    # matches the logged-in user
    if expense.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only add expenses to your own account"
        )

    database.add_expense(
        user_id,
        expense.amount,
        expense.category,
        expense.description
    )

    expenses = database.get_expenses(
        user_id
    )

    new_expense = expenses[-1]

    return {
        "id": new_expense[0],
        "amount": new_expense[1],
        "category": new_expense[2],
        "description": new_expense[3]
    }


# ==========================================
# UPDATE EXPENSE
# ==========================================

@app.put(
    "/expenses/{expense_id}",
    response_model=ExpenseResponse
)
def update_expense(
    expense_id: int,
    expense: Expense,
    current_user=Depends(get_current_user)
):

    user_id = current_user[0]

    if expense.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own expenses"
        )

    updated = database.update_expense(
        user_id,
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
        "id": expense_id,
        "amount": expense.amount,
        "category": expense.category,
        "description": expense.description
    }


# ==========================================
# DELETE EXPENSE
# ==========================================

@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    current_user=Depends(get_current_user)
):

    user_id = current_user[0]

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
        "message": "Expense deleted successfully"
    }


# ==========================================
# FINANCIAL DASHBOARD
# ==========================================

@app.get(
    "/users/{user_id}/dashboard",
    response_model=DashboardResponse
)
def get_dashboard(user_id: int):

    user = database.get_user(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    expenses = database.get_expenses(
        user_id
    )

    total_expenses = sum(
        expense[1]
        for expense in expenses
    )

    balance = user[2] - total_expenses

    # Spending by category
    spending_by_category = {}

    for expense in expenses:

        category = expense[2]
        amount = expense[1]

        if category not in spending_by_category:
            spending_by_category[category] = 0

        spending_by_category[category] += amount

    # Highest spending category
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

    # Savings rate
    if user[2] > 0:

        savings_rate = (
            balance / user[2]
        ) * 100

    else:

        savings_rate = 0

    # Spending warning
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

        "spending_by_category":
            spending_by_category,

        "highest_spending_category": {
            "category": highest_category,
            "amount": highest_amount
        },

        "warning": warning
    }