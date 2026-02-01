from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import AccountDB, TransactionDB
from app.repositories.account_repository import AccountRepository

class BankService:

    def __init__(self):
        self.repo = AccountRepository()

    def create_account(self, db: Session, account_id: str, initial_balance: float):
        existing = self.repo.get(db, account_id)
        if existing:
            raise HTTPException(status_code=400, detail="Account already exists")

        new_acc = AccountDB(
            account_id=account_id,
            balance=initial_balance
        )
        return self.repo.create(db, new_acc)

    def deposit(self, db: Session, account_id: str, amount: float, currency: str, description: str):
        account = self.repo.get(db, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        if amount <= 0:
            raise HTTPException(status_code=400, detail="Deposit amount must be positive")

        # Ajustar balance
        account.balance += amount

        tx = TransactionDB(
            type="DEPOSIT",
            amount=amount,
            currency=currency,
            description=description,
            account_id=account_id
        )

        self.repo.save(db, tx)

        # Persistimos cambio en account también
        self.repo.save(db, account)
        return account

    def withdraw(self, db: Session, account_id: str, amount: float, currency: str, description: str):
        account = self.repo.get(db, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        if amount <= 0:
            raise HTTPException(status_code=400, detail="Withdraw amount must be positive")
        if amount > account.balance:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        account.balance -= amount

        tx = TransactionDB(
            type="WITHDRAW",
            amount=amount,
            currency=currency,
            description=description,
            account_id=account_id
        )

        self.repo.save(db, tx)
        self.repo.save(db, account)

        return account

    def get_transactions(self, db: Session, account_id: str):
        return self.repo.list_transactions(db, account_id)
