import sqlite3

from fastapi import APIRouter, HTTPException

from app import database

from app.auth import (
    hash_password,
    verify_password,
    create_access_token
)

from app.logging_config import logger

from app.api.schemas import (
    User,
    LoginRequest,
    UserCreatedResponse
)


router = APIRouter(
    tags=["Authentication"]
)


# ==========================================
# CREATE USER
# ==========================================

@router.post(
    "/users",
    response_model=UserCreatedResponse,
    summary="Create a new user"
)
def create_user(user: User):

    # Check username
    existing_user = database.get_user_by_name(
        user.name
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Check email
    existing_email = database.get_user_by_email(
        user.email
    )

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Hash password
    hashed_password = hash_password(
        user.password
    )

    try:

        user_id = database.create_user(
            name=user.name,
            income=user.income,
            password=hashed_password,
            email=str(user.email)
        )

    except sqlite3.IntegrityError:

        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    logger.info(
        f"New user created: {user.name}"
    )

    return {
        "id": user_id,
        "name": user.name,
        "income": user.income,
        "email": user.email
    }


# ==========================================
# LOGIN
# ==========================================

@router.post(
    "/login",
    summary="Login to BudgetWise"
)
def login(login_data: LoginRequest):

    # Find user by username
    user = database.get_user_by_name(
        login_data.name
    )

    # User does not exist
    if user is None:

        logger.warning(
            f"Login failed: user not found - "
            f"{login_data.name}"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Database structure:
    #
    # user[0] = id
    # user[1] = name
    # user[2] = income
    # user[3] = password
    # user[4] = email

    stored_password = user[3]

    # Verify password
    password_is_correct = verify_password(
        login_data.password,
        stored_password
    )

    if not password_is_correct:

        logger.warning(
            f"Login failed: incorrect password - "
            f"{login_data.name}"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Create JWT token
    access_token = create_access_token(
        user[0]
    )

    logger.info(
        f"User logged in successfully: "
        f"{login_data.name}"
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }
