import unittest
from entities.monthly_expense import MonthlyExpenses

class TestMonthlyExpense(unittest.TestCase):

    def test_monthly_expense(self):
        self.assertAlmostEqual(MonthlyExpenses('rent', 2000, 12).name, 'rent')
        self.assertAlmostEqual(MonthlyExpenses('rent', 2000, 12).amount, 2000)
        self.assertAlmostEqual(MonthlyExpenses('rent', 2000, 12).date, 12)

        with self.assertRaises(AssertionError):
            MonthlyExpenses(2000, 12)
            MonthlyExpenses('rent', -2000, 12)
            MonthlyExpenses('rent', 2000, 1.2)

        with self.assertRaises(ValueError):
            MonthlyExpenses('rent', 2000, 35)