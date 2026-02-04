from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import AccountDB, TransactionDB
from app.repositories.account_repository import AccountRepository
from app.core.logger import logger
from typing import List, Optional
from datetime import datetime

class BankService:
    def __init__(self):
        self.repo = AccountRepository()

    async def create_account(self, db: AsyncSession, account_id: str, initial_balance: float):
        logger.info(f"Creating account {account_id} with balance {initial_balance}")
        account = await self.repo.get(db, account_id)
        if account:
            raise HTTPException(status_code=400, detail="Account already exists")
        return await self.repo.create(db, account_id, initial_balance)

    async def deposit(self, db: AsyncSession, account_id: str, amount: float, currency: str, description: str):
        logger.info(f"Depositing {amount} {currency} to {account_id}")
        account = await self.repo.get(db, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return await self.repo.deposit(db, account, amount, currency, description)

    async def withdraw(self, db: AsyncSession, account_id: str, amount: float, currency: str, description: str):
        logger.info(f"Withdrawing {amount} {currency} from {account_id}")
        account = await self.repo.get(db, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        if account.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        return await self.repo.withdraw(db, account, amount, currency, description)

    async def get_transactions(
        self, db: AsyncSession, account_id: str, 
        type_: Optional[str] = None, 
        start: Optional[datetime] = None, 
        end: Optional[datetime] = None
    ) -> List[TransactionDB]:
        account = await self.repo.get(db, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        transactions = await self.repo.list_transactions(db, account_id)
        
        # Filtrar por tipo
        if type_:
            transactions = [t for t in transactions if t.type_ == type_]
        # Filtrar por rango de fechas
        if start:
            transactions = [t for t in transactions if t.timestamp >= start]
        if end:
            transactions = [t for t in transactions if t.timestamp <= end]
        return transactions
