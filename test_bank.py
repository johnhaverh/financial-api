def test_bank_info(self):
        bank = Bank(name="Test Bank", country="Test Country", established_year=2000)
        info = bank.get_bank_info()
        self.assertEqual(info["name"], "Test Bank")
        self.assertEqual(info["country"], "Test Country")
        self.assertEqual(info["established_year"], 2000)

from financial_api.bank import Bank

import unittest 
class TestBank(unittest.TestCase):
    def test_bank_initialization(self):
        bank = Bank(name="Test Bank", country="Test Country", established_year=2000)
        self.assertEqual(bank.name, "Test Bank")
        self.assertEqual(bank.country, "Test Country")
        self.assertEqual(bank.established_year, 2000)
    def test_bank_info(self):
        bank = Bank(name="Test Bank", country="Test Country", established_year=2000)
        info = bank.get_bank_info()
        self.assertEqual(info["name"], "Test Bank")
        self.assertEqual(info["country"], "Test Country")
        self.assertEqual(info["established_year"], 2000)
    def test_bank_initialization(self):
        bank = Bank(name="Test Bank", country="Test Country", established_year=2000)
        self.assertEqual(bank.name, "Test Bank")
        self.assertEqual(bank.country, "Test Country")
        self.assertEqual(bank.established_year, 2000)
        