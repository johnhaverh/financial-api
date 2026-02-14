import pytest
from fastapi.testclient import TestClient
from app.api.api import app
import asyncio
from app.db.database import engine, Base

# Global counter for unique account names
_test_counter = 0

def setup_function():
    """Setup before each test"""
    asyncio.run(init_db_async())

def teardown_function():
    """Cleanup after each test"""
    asyncio.run(drop_db_async())

async def init_db_async():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db_async():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

def get_unique_id(name: str) -> str:
    """Get a unique account ID for testing"""
    global _test_counter
    _test_counter += 1
    return f"{name}_{_test_counter}"

client = TestClient(app)

def test_create_account():
    response = client.post("/accounts", json={"account_id": "acc1", "initial_balance": 100})
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 100
    assert data["account_id"] == "acc1"

def test_deposit():
    client.post("/accounts", json={"account_id": "acc2", "initial_balance": 0})
    response = client.post("/accounts/acc2/deposit", json={
        "type_": "deposit",
        "amount": 50,
        "currency": "USD",
        "description": "Initial deposit"
    })
    assert response.status_code == 200
    assert response.json()["balance"] == 50

def test_withdraw_insufficient():
    client.post("/accounts", json={"account_id": "acc3", "initial_balance": 10})
    response = client.post("/accounts/acc3/withdraw", json={
        "type_": "withdraw",
        "amount": 20,
        "currency": "USD",
        "description": "Trying to overdraft"
    })
    assert response.status_code == 400

def test_get_balance():
    client.post("/accounts", json={"account_id": "acc_balance", "initial_balance": 200})
    response = client.get("/accounts/acc_balance/balance")
    assert response.status_code == 200
    assert response.json()["balance"] == 200

def test_transactions_created():
    client.post("/accounts", json={"account_id": "acc4", "initial_balance": 0})
    client.post("/accounts/acc4/deposit", json={
        "type_": "deposit",
        "amount": 10,
        "currency": "USD",
        "description": "Deposit 10"
    })
    client.post("/accounts/acc4/deposit", json={
        "type_": "deposit",
        "amount": 15,
        "currency": "USD",
        "description": "Deposit 15"
    })
    response = client.get("/accounts/acc4/transactions")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_transaction_validation():
    client.post("/accounts", json={"account_id": "acc5", "initial_balance": 0})

    # Invalid transaction type
    response = client.post("/accounts/acc5/deposit", json={
        "type_": "invalid",
        "amount": 100,
        "currency": "USD",
        "description": "Test invalid type"
    })
    assert response.status_code == 422

    # Negative amount
    response = client.post("/accounts/acc5/deposit", json={
        "type_": "deposit",
        "amount": -50,
        "currency": "USD",
        "description": "Test negative amount"
    })
    assert response.status_code == 422

def test_account_summary():
    client.post("/accounts", json={"account_id": "acc10", "initial_balance": 0})
    
    client.post("/accounts/acc10/deposit", json={
        "type_": "deposit",
        "amount": 100,
        "currency": "USD",
        "description": "salary"
    })

    client.post("/accounts/acc10/withdraw", json={
        "type_": "withdraw",
        "amount": 40,
        "currency": "USD",
        "description": "groceries"
    })

    response = client.get("/accounts/acc10/summary")
    data = response.json()

    assert response.status_code == 200
    assert data["balance"] == 60
    assert data["total_deposits"] == 100
    assert data["total_withdrawals"] == 40
    assert data["transaction_count"] == 2