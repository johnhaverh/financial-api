# bank.py

from dataclasses import dataclass, field
from typing import Dict
from models.account import Account

@dataclass
class Bank:
    name: str
    country: str
    established_year: int

    accounts: Dict[str, Account] = field(default_factory=dict)

    def create_account(self, account_id: str, initial_balance: float = 0) -> Account:
        if account_id in self.accounts:
            raise ValueError("Account already exists")
        account = Account(account_id, initial_balance)
        self.accounts[account_id] = account
        return account

    def get_account(self, account_id: str) -> Account:
        return self.accounts.get(account_id)

    def delete_account(self, account_id: str) -> bool:
        if account_id in self.accounts:
            del self.accounts[account_id]
            return True
        return False
    
    def __repr__(self):
        return f"\n Name: {self.name} \n Country: {self.country} \n Established Year: {self.established_year} \n "

# Ejemplo de uso
if __name__ == "__main__":
    bank = Bank("Global Bank", "USA", 1990)
    print("Bank info:", bank)
    acc1 = bank.create_account("1234", 100)
    acc1.deposit(50)
    acc1.withdraw(30)
    print(acc1.get_transactions())
    