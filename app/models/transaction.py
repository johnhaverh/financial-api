from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Transaction:

    type_: str
    transaction_id: int
    amount: float
    currency: str
    description: str
    timestamp: datetime = field(default_factory=datetime.now)

    def __repr__(self):
        return f"Type: {self.type_} ID: {self.transaction_id} Amount: {self.amount} {self.currency} Description: {self.description} Timestamp: {self.timestamp} \n"
