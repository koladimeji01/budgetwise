from pydantic import BaseModel, Field, EmailStr


# ==========================================
# EXPENSE REQUEST
# ==========================================

class ExpenseCreate(BaseModel):

    amount: float = Field(
        gt=0,
        description="Expense amount in Nigerian Naira."
    )

    category: str = Field(
        min_length=2,
        max_length=50,
        description="Expense category."
    )

    description: str = Field(
        min_length=2,
        max_length=200,
        description="Short description of the expense."
    )


# ==========================================
# USER REQUEST
# ==========================================

class User(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=50,
        description="Username for the BudgetWise account."
    )

    email: EmailStr = Field(
        description="User email address."
    )

    income: float = Field(
        gt=0,
        description="Monthly income in Nigerian Naira."
    )

    password: str = Field(
        min_length=8,
        max_length=100,
        description="Account password."
    )


# ==========================================
# LOGIN REQUEST
# ==========================================

class LoginRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=50,
        description="BudgetWise username."
    )

    password: str = Field(
        min_length=8,
        max_length=100,
        description="Account password."
    )


# ==========================================
# EXPENSE RESPONSE
# ==========================================

class ExpenseResponse(BaseModel):

    id: int
    amount: float
    category: str
    description: str


# ==========================================
# EXPENSE LIST RESPONSE
# ==========================================

class ExpenseListResponse(BaseModel):

    user_id: int
    expenses: list[ExpenseResponse]


# ==========================================
# USER CREATED RESPONSE
# ==========================================

class UserCreatedResponse(BaseModel):

    id: int
    name: str
    income: float
    email: EmailStr


# ==========================================
# USER PROFILE RESPONSE
# ==========================================

class UserResponse(BaseModel):

    id: int
    name: str
    income: float
    email: EmailStr | None
    total_expenses: float
    balance: float
    expenses: list[ExpenseResponse]


# ==========================================
# DASHBOARD USER
# ==========================================

class DashboardUser(BaseModel):

    id: int
    name: str
    income: float
    email: EmailStr | None


# ==========================================
# HIGHEST SPENDING CATEGORY
# ==========================================

class HighestSpendingCategory(BaseModel):

    category: str | None
    amount: float


# ==========================================
# DASHBOARD RESPONSE
# ==========================================

class DashboardResponse(BaseModel):

    user: DashboardUser

    income: float

    total_expenses: float

    balance: float

    savings_rate: float

    spending_by_category: dict[str, float]

    highest_spending_category: HighestSpendingCategory

    warning: str