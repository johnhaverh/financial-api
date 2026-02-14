from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db
from app.schemas.account import AccountCreate
from app.schemas.transaction import TransactionRequest
from app.services.bank_service import BankService
from app.core.middleware import MetricsMiddleware
from app.core.logger import logger
from typing import Optional
from datetime import datetime

app = FastAPI(title="Financial API v2")

# Integrar middleware de métricas
app.add_middleware(MetricsMiddleware)

bank_service = BankService()

@app.post("/accounts")
async def create_account(request: AccountCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating account {request.account_id}")
    acc = await bank_service.create_account(db, request.account_id, request.initial_balance)
    return {"account_id": acc.account_id, "balance": acc.balance}

@app.post("/accounts/{account_id}/deposit")
async def deposit(account_id: str, request: TransactionRequest, db: AsyncSession = Depends(get_db)):
    logger.info(f"Deposit {request.amount} {request.currency} to {account_id}")
    acc = await bank_service.deposit(db, account_id, request.amount, request.currency, request.description)
    return {"balance": acc.balance}

@app.post("/accounts/{account_id}/withdraw")
async def withdraw(account_id: str, request: TransactionRequest, db: AsyncSession = Depends(get_db)):
    logger.info(f"Withdraw {request.amount} {request.currency} from {account_id}")
    acc = await bank_service.withdraw(db, account_id, request.amount, request.currency, request.description)
    return {"balance": acc.balance}

@app.get("/accounts/{account_id}/balance")
async def get_balance(account_id: str, db: AsyncSession = Depends(get_db)):
    account = await bank_service.repo.get(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"balance": account.balance}

@app.get("/accounts/{account_id}/transactions")
async def get_transactions(
    account_id: str, 
    type_: Optional[str] = None, 
    start: Optional[datetime] = None, 
    end: Optional[datetime] = None, 
    db: AsyncSession = Depends(get_db)
):
    return await bank_service.get_transactions(db, account_id, type_, start, end)

@app.get("/accounts/{account_id}/summary")
async def account_summary(account_id: str, db: AsyncSession = Depends(get_db)):
    return await bank_service.get_account_summary(db, account_id)