from sqlalchemy.orm import Session
from app.db.models import AccountDB, TransactionDB

class AccountRepository:

    def get(self, db: Session, account_id: str) -> AccountDB | None:
        return db.query(AccountDB).filter(AccountDB.account_id == account_id).first()

    def create(self, db: Session, account: AccountDB) -> AccountDB:
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    def save(self, db: Session, entity):
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def list_transactions(self, db: Session, account_id: str):
        return db.query(TransactionDB).filter(TransactionDB.account_id == account_id).all()
    
    def add_transaction(self, db: Session, transaction: TransactionDB) -> TransactionDB:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    
    def get_by_id(self, db: Session, account_id: str) -> AccountDB | None:
        return db.query(AccountDB).filter_by(account_id=account_id).first()
    
    def update_balance(self, db: Session, account: AccountDB, new_balance: float) -> AccountDB:
        account.balance = new_balance
        db.commit()
        db.refresh(account)
        return account