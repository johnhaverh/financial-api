from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.account import AccountCreate
from app.schemas.transaction import TransactionRequest
from app.services.bank_service import BankService

app = FastAPI(title="Financial API v2")

bank_service = BankService()

# @app.post("/accounts", status_code=201)
@app.post("/accounts")
def create_account(request: AccountCreate, db: Session = Depends(get_db)):
    acc = bank_service.create_account(
        db,
        request.account_id,
        request.initial_balance
    )
    return {"account_id": acc.account_id, "balance": acc.balance}


@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: str, request: TransactionRequest, db: Session = Depends(get_db)):
    acc = bank_service.deposit(
        db,
        account_id,
        request.amount,
        request.currency,
        request.description
    )
    return {"balance": acc.balance}


@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str, request: TransactionRequest, db: Session = Depends(get_db)):
    acc = bank_service.withdraw(
        db,
        account_id,
        request.amount,
        request.currency,
        request.description
    )
    return {"balance": acc.balance}


@app.get("/accounts/{account_id}/balance")
def get_balance(account_id: str, db: Session = Depends(get_db)):
    account = bank_service.repo.get(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"balance": account.balance}


@app.get("/accounts/{account_id}/transactions")
def get_transactions(account_id: str, db: Session = Depends(get_db)):
    return bank_service.get_transactions(db, account_id)
