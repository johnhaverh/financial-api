# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.db.dependencies import get_db
# from app.db.models import AccountDB, TransactionDB
# from app.schemas.account import AccountCreate
# from app.schemas.transaction import TransactionRequest, TransactionResponse

# app = FastAPI()

# @app.post("/accounts")
# def create_account(
#     request: AccountCreate,
#     db: Session = Depends(get_db)
# ):
#     if db.query(AccountDB).filter_by(account_id=request.account_id).first():
#         raise HTTPException(status_code=400, detail="Account already exists")

#     account = AccountDB(
#         account_id=request.account_id,
#         balance=request.initial_balance
#     )

#     db.add(account)
#     db.commit()
#     db.refresh(account)
#     return {"account_id": account.account_id, "balance": account.balance}


# @app.post("/accounts/{account_id}/deposit")
# def deposit(
#     account_id: str,
#     tx: TransactionRequest,
#     db: Session = Depends(get_db)
# ):
#     account = db.query(AccountDB).filter_by(account_id=account_id).first()
#     if not account:
#         raise HTTPException(status_code=404, detail="Account not found")
    
#     try:
#         if tx.amount <= 0:
#             raise ValueError("Deposit amount must be positive")
        
#         account.balance += tx.amount
        
#         transaction = TransactionDB(
#             type="DEPOSIT",
#             amount=tx.amount,
#             currency=tx.currency,
#             description=tx.description,
#             account_id=account_id
#         )
        
#         db.add(transaction)
#         db.commit()
#         db.refresh(account)
        
#         return {"balance": account.balance, "transactions": len(account.transactions)}
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @app.post("/accounts/{account_id}/withdraw")
# def withdraw(
#     account_id: str,
#     tx: TransactionRequest,
#     db: Session = Depends(get_db)
# ):
#     account = db.query(AccountDB).filter_by(account_id=account_id).first()
#     if not account:
#         raise HTTPException(status_code=404, detail="Account not found")
    
#     try:
#         if tx.amount <= 0:
#             raise ValueError("Withdrawal amount must be positive")
#         if tx.amount > account.balance:
#             raise ValueError("Insufficient funds")
        
#         account.balance -= tx.amount
        
#         transaction = TransactionDB(
#             type="WITHDRAW",
#             amount=tx.amount,
#             currency=tx.currency,
#             description=tx.description,
#             account_id=account_id
#         )
        
#         db.add(transaction)
#         db.commit()
#         db.refresh(account)
        
#         return {"balance": account.balance, "transactions": len(account.transactions)}
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @app.get("/accounts/{account_id}/balance")
# def get_balance(
#     account_id: str,
#     db: Session = Depends(get_db)
# ):
#     account = db.query(AccountDB).filter_by(account_id=account_id).first()
#     if not account:
#         raise HTTPException(status_code=404, detail="Account not found")
#     return {"account_id": account.account_id, "balance": account.balance}


# @app.get("/accounts/{account_id}/transactions")
# def get_transactions(
#     account_id: str,
#     db: Session = Depends(get_db)
# ):
#     account = db.query(AccountDB).filter_by(account_id=account_id).first()
#     if not account:
#         raise HTTPException(status_code=404, detail="Account not found")
    
#     transactions = db.query(TransactionDB).filter_by(account_id=account_id).all()
#     return [
#         {
#             "type": t.type,
#             "amount": t.amount,
#             "currency": t.currency,
#             "description": t.description,
#             "timestamp": t.timestamp
#         }
#         for t in transactions
#     ]
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
