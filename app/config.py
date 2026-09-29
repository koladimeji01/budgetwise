import os

from dotenv import load_dotenv


# ==========================================
# DETECT ENVIRONMENT
# ==========================================

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development"
).lower()


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

if ENVIRONMENT == "testing":

    load_dotenv(
        ".env.test"
    )

elif ENVIRONMENT == "development":

    load_dotenv(
        ".env"
    )


# ==========================================
# APPLICATION SETTINGS
# ==========================================

APP_NAME = os.getenv(
    "APP_NAME",
    "BudgetWise"
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0"
)


# ==========================================
# DATABASE
# ==========================================

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "budgetwise.db"
)


# ==========================================
# AUTHENTICATION
# ==========================================

SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)


# ==========================================
# SECURITY CHECK
# ==========================================

if ENVIRONMENT == "production":

    if not SECRET_KEY:

        raise RuntimeError(
            "SECRET_KEY must be configured "
            "in production."
        )


# ==========================================
# ENVIRONMENT INFORMATION
# ==========================================

print(
    f"BudgetWise environment: {ENVIRONMENT}"
)