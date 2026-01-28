from datetime import datetime
class Transaction:
    def __init__(self, type_, transaction_id, amount, currency, description,timestamp=None):
        self.type = type_
        self.transaction_id = transaction_id
        self.amount = amount
        self.currency = currency
        self.description = description
        #self.timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S") # Format datetime to string
        self.timestamp = timestamp or datetime.now()

    def to_dict(self):
        return {
            "type": self.type,
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "currency": self.currency,
            "description": self.description,
            "timestamp": self.timestamp,
        }
    
    def __repr__(self):
        return f"{self.timestamp} - {self.type}: {self.amount}"
    