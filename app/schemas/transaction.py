from pydantic import BaseModel, Field
from datetime import datetime

class TransactionRequest(BaseModel):
    type_: str = Field(..., pattern="^(deposit|withdraw)$")
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    description: str = Field(..., min_length=1, max_length=255)
    timestamp: datetime = Field(default_factory=datetime.now)
