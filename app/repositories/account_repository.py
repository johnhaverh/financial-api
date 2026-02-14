from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import AccountDB, TransactionDB
from datetime import datetime

class AccountRepository:

    async def get(self, db: AsyncSession, account_id: str):
        result = await db.execute(
            select(AccountDB).where(AccountDB.account_id == account_id)
        )
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, account_id: str, initial_balance: float):
        account = AccountDB(account_id=account_id, balance=initial_balance)
        db.add(account)
        await db.commit()
        await db.refresh(account)
        return account

    async def save(self, db: AsyncSession, entity):
        db.add(entity)
        await db.commit()
        await db.refresh(entity)
        return entity

    async def deposit(self, db: AsyncSession, account: AccountDB, amount: float, currency: str, description: str):
        account.balance += amount
        transaction = TransactionDB(
            account_id=account.account_id,
            type_="deposit",
            amount=amount,
            currency=currency,
            description=description,
            timestamp=datetime.now()
        )
        db.add(transaction)
        await self.save(db, account)
        return account

    async def withdraw(self, db: AsyncSession, account: AccountDB, amount: float, currency: str, description: str):
        account.balance -= amount
        transaction = TransactionDB(
            account_id=account.account_id,
            type_="withdraw",
            amount=amount,
            currency=currency,
            description=description,
            timestamp=datetime.now()
        )
        db.add(transaction)
        await self.save(db, account)
        return account

    async def list_transactions(self, db: AsyncSession, account_id: str):
        result = await db.execute(
            select(TransactionDB).where(TransactionDB.account_id == account_id)
        )
        return result.scalars().all()

    async def get_summary(self, db: AsyncSession, account_id: str) -> dict:
        account = await self.get(db, account_id)
        if not account:
            return None
        
        transactions = await self.list_transactions(db, account_id)
        
        deposits = sum(
            t.amount for t in transactions if t.type_ == "deposit"
        )
        withdrawals = sum(
            t.amount for t in transactions if t.type_ == "withdraw"
        )
        
        return {
            "account_id": account.account_id,
            "balance": account.balance,
            "total_deposits": deposits,
            "total_withdrawals": withdrawals,
            "transaction_count": len(transactions)
        }