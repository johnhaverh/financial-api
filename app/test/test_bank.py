import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from bank import Bank

class TestBank(unittest.TestCase):
    def setUp(self):
        self.bank = Bank("Global Bank", "USA", 1990)
        self.acc = self.bank.create_account("1234", 100)

    def test_deposit(self):
        self.acc.deposit(50)
        self.assertEqual(self.acc.balance, 150)

    def test_withdraw(self):
        self.acc.withdraw(40)
        self.assertEqual(self.acc.balance, 60)

    def test_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(200)

    def test_account_creation_duplicate(self):
        with self.assertRaises(ValueError):
            self.bank.create_account("1234")
    
    def test_negative_deposit(self):
        with self.assertRaises(ValueError):
            self.acc.deposit(-50)

    def test_invalid_deposit_type(self):
        with self.assertRaises(TypeError):
            self.acc.deposit("100")

    def test_balance_is_read_only(self):
        with self.assertRaises(AttributeError):
            self.acc.balance = 1000

    def test_invalid_transaction_type(self):
        from models.transaction import Transaction
        with self.assertRaises(ValueError):
            Transaction("TRANSFER", 1, 100, "USD", "Transfer")

    def test_transaction_is_immutable(self):
        from models.transaction import Transaction
        tx = Transaction("DEPOSIT", 1, 100, "USD", "Deposit")
        with self.assertRaises(Exception):
            tx.amount = 200
            
if __name__ == "__main__":
    unittest.main()
