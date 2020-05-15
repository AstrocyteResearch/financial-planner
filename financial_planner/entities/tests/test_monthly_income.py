import unittest
from entities.monthly_income import MonthlyIncome

class TestMonthlyIncome(unittest.TestCase):

    def test_monthly_income(self):
        self.assertAlmostEqual(MonthlyIncome(40000, 0.02, 0.01, 12).salary, 40000)
        self.assertAlmostEqual(MonthlyIncome(40000, 0.02, 0.01, 12).salary_growth_rate, 0.02)
        self.assertAlmostEqual(MonthlyIncome(40000, 0.02, 0.01, 12).savings_rate, 0.01)
        self.assertAlmostEqual(MonthlyIncome(40000, 0.02, 0.01, 12).date, 12)

        with self.assertRaises(AssertionError):
            MonthlyIncome(-1, 0.02, 0.01, 12)
            MonthlyIncome(40000, -0.02, 0.01, 12)
            MonthlyIncome(40000, 0.02, -0.01, 12)
            MonthlyIncome(40000, 0.02, 0.01, 1.2)

        with self.assertRaises(ValueError):
            MonthlyIncome(40000, 0.02, 0.01, 35)
