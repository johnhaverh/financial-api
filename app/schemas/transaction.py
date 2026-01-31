from datetime import datetime
from pydantic import BaseModel

class TransactionRequest(BaseModel):
    type_: str
    transaction_id: int
    amount: float
    currency: str
    description: str
    timestamp: datetime = None
