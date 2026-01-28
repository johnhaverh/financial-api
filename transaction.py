class Transaction:
    def __init__(self, transaction_id, amount, currency, date, description):
        self.transaction_id = transaction_id
        self.amount = amount
        self.currency = currency
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "currency": self.currency,
            "date": self.date,
            "description": self.description,
        }