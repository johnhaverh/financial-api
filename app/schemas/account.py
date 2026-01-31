from datetime import datetime
from pydantic import BaseModel

class AccountCreate(BaseModel):
    account_id: str
    initial_balance: float = 0

