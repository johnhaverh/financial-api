# bank.py

from models.account import Account

class Bank:
    def __init__(self, name, country, established_year):
        self.name = name
        self.country = country
        self.established_year = established_year
        self.accounts = {}

    def get_bank_info(self):
        return {
            "name": self.name,
            "country": self.country,
            "established_year": self.established_year
        }
    
    def create_account(self, account_id, initial_balance=0):
        if account_id in self.accounts:
            raise ValueError("Account already exists")
        self.accounts[account_id] = Account(account_id, initial_balance)
        return self.accounts[account_id]

    def get_account(self, account_id):
        return self.accounts.get(account_id)

    def delete_account(self, account_id):
        if account_id in self.accounts:
            del self.accounts[account_id]
            return True
        return False
    
    def __repr__(self):
        return f"Name: {self.name} Country: {self.country} Established Year: {self.established_year}"

# Example usage
if __name__ == "__main__":
    bank =Bank("Global Bank", "USA", 1990)
    #print("Bank info:", bank.get_bank_info())
    print("Bank info:", bank)

    acc = bank.create_account("1234", 100)
    print("Account Info: ",bank.get_account("1234"))
    print("Initial Balance:", acc.balance)
    acc.deposit(50)
    print("Balance after depositing 50:", acc.balance)
    acc.withdraw(30)
    print("Balance after withdrawing 30:", acc.balance)
    print(acc.get_transactions())
    bank.delete_account("1234")
    print("Account deleted.")
    print("Account Info: ",bank.get_account("1234"))
    