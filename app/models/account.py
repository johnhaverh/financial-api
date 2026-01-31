from dataclasses import dataclass, field
from typing import List
from app.models.transaction import Transaction

@dataclass
class Account:
    account_id: str
    _balance: float = 0
    transactions: List[Transaction] = field(default_factory=list)

    def __post_init__(self):
        if not self.account_id:
            raise ValueError("Account ID is required")
        if self._balance < 0:
            raise ValueError("Initial balance cannot be negative")

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float, currency="USD", description="Deposit"):
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount number must be numeric")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        tx = Transaction(
            type_="DEPOSIT",
            transaction_id=len(self.transactions) + 1,
            amount=amount,
            currency=currency,
            description=description,
        )

        self._balance += amount
        self.transactions.append(tx)
        return self._balance

    def withdraw(self, amount: float, currency="USD", description="Withdraw"):
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be numeric")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        
        tx = Transaction(
            type_="WITHDRAW",
            transaction_id=len(self.transactions) + 1,
            amount=amount,
            currency=currency,
            description=description,
        )
            
        self._balance -= amount
        self.transactions.append(tx)
        return self._balance
    
    def get_balance_summary(self) -> float:
        return self._balance
    
    def get_transactions(self) -> List[Transaction]:
        return self.transactions
    
    def __repr__(self):
        return f"Account({self.account_id}, balance={self._balance})"