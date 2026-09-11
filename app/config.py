import os

from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


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
# DATABASE SETTINGS
# ==========================================

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "budgetwise.db"
)


# ==========================================
# JWT SETTINGS
# ==========================================

SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)
