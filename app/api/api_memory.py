from fastapi import FastAPI, HTTPException
from app.models.bank import Bank
from app.schemas.account import AccountCreate
from app.schemas.transaction import TransactionRequest, TransactionResponse

bank = Bank("Global Bank", "USA", 1990)

app = FastAPI(
    title="Banking API",
    description=f"{bank.name} - {bank.country}",
    version="1.0.0"
)


@app.post("/accounts")
def create_account(data: AccountCreate):
    try:
        acc = bank.create_account(data.account_id, data.initial_balance)
        return {"account_id": acc.account_id, "balance": acc.balance}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: str, tx: TransactionRequest):
    acc = bank.get_account(account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    try:
        acc.deposit(tx.amount, tx.currency, tx.description)
        return {"balance": acc.balance,
                "transactions": len(acc.transactions)
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str, tx: TransactionRequest):
    acc = bank.get_account(account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    try:
        acc.withdraw(tx.amount, tx.currency, tx.description)
        return {"balance": acc.balance,
                "transactions": len(acc.transactions)
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/accounts/{account_id}/balance")
def get_balance(account_id: str):
    acc = bank.get_account(account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    # return {"balance": acc.get_balance_summary()}
    return {"balance": acc.balance}


@app.get("/accounts/{account_id}/transactions")
def get_transactions(account_id: str):
    acc = bank.get_account(account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    return [TransactionResponse(**tx.__dict__) for tx in acc.transactions]