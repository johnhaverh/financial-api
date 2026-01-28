from transaction import Transaction
class Account:
    def __init__(self, account_id, balance=0.0):
        self.account_id = account_id
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transactions.append(Transaction("DEPOSIT", 1, amount, "USD", "Deposit"))
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.transactions.append(Transaction("WITHDRAW", 1, amount, "USD", "Withdrawal"))
        return self.balance

    def get_balance(self):
        return self.balance

    def get_account_info(self):
        return {
            "account_id": self.account_id,
            "balance": self.balance
        }
    
    def get_transactions(self):
        return self.transactions
    
    def __repr__(self):
        return f"Id: {self.account_id} Balance: {self.balance}"
    
class SavingsAccount(Account):
    def __init__(self, account_id, balance=0.0, interest_rate=0.01):
        super().__init__(account_id, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        return self.balance
    def get_account_info(self):
        info = super().get_account_info()
        info["interest_rate"] = self.interest_rate
        return info
    
class CheckingAccount(Account):
    def __init__(self, account_id, balance=0.0, overdraft_limit=0.0):
        super().__init__(account_id, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance + self.overdraft_limit:
            raise ValueError("Insufficient funds including overdraft limit.")
        self.balance -= amount
        return self.balance
    def get_account_info(self):
        info = super().get_account_info()
        info["overdraft_limit"] = self.overdraft_limit
        return info
