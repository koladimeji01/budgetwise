import sys
from pathlib import Path

from fastapi.testclient import TestClient


# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


from api import app


client = TestClient(app)


# ==========================================
# TEST HOME PAGE
# ==========================================

def test_home():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Welcome to BudgetWise API"


# ==========================================
# TEST HEALTH CHECK
# ==========================================

def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


# ==========================================
# TEST USER REGISTRATION
# ==========================================

def test_create_user():

    response = client.post(
        "/users",
        json={
            "name": "testuser",
            "income": 300000,
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["name"] == "testuser"
    assert data["income"] == 300000

    # Password must never be returned
    assert "password" not in data