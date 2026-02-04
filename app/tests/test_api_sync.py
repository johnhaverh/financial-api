import pytest
from fastapi.testclient import TestClient
from app.api.api import app
from app.db.database import Base, engine

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    # Drop all tables and recreate them for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_create_account():
    response = client.post("/accounts", json={"account_id": "acc1", "initial_balance": 100})
    assert response.status_code == 200
    data = response.json()
    assert data["account_id"] == "acc1"
    assert data["balance"] == 100


def test_deposit():
    client.post("/accounts", json={"account_id": "acc2", "initial_balance": 50})

    response = client.post(
        "/accounts/acc2/deposit",
        json={
            "amount": 25,
            "currency": "USD",
            "description": "Initial deposit"
        }
    )

    assert response.status_code == 200
    assert response.json()["balance"] == 75


def test_withdraw_insufficient():
    client.post("/accounts", json={"account_id": "acc3", "initial_balance": 20})

    response = client.post(
        "/accounts/acc3/withdraw",
        json={
            "amount": 100,
            "currency": "USD",
            "description": "ATM withdraw"
        }
    )

    assert response.status_code == 400
    assert "Insufficient" in response.json()["detail"]


def test_transactions_created():
    client.post("/accounts", json={"account_id": "acc4", "initial_balance": 0})

    client.post("/accounts/acc4/deposit", json={"amount": 10})
    client.post("/accounts/acc4/deposit", json={"amount": 15})

    response = client.get("/accounts/acc4/transactions")
    assert response.status_code == 200
    assert len(response.json()) == 2
