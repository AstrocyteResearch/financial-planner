import unittest
from calculators.Cash_Flow_Analysis.Cash_Flow_Analysis import CashFlow
from entities.household import Person
from entities.monthly_income import MonthlyIncome
from entities.expense import Expenses
from entities.monthly_expense import MonthlyExpenses


class TestCashFlowAnalysis(unittest.TestCase):

    def test_assignment(self):
        person = Person(
            age=30,
            gender='M'
        )
        person.add_job(MonthlyIncome(salary=20000, salary_growth_rate=0.0015, date=28))
        person.add_expense(Expenses('living expenses', amount=3000))
        person.add_expense(MonthlyExpenses('credit card payment', amount=3000, date=15))
        person.add_expense(MonthlyExpenses('rents', amount=2000, date=1))
        self.person = person
        self.assertAlmostEqual(CashFlow(person).person, person)
        self.assertAlmostEqual(CashFlow(person).salary_growth_rate, 0.0015)
        self.assertAlmostEqual(CashFlow(person).income, person.income[0])
        self.assertAlmostEqual(CashFlow(person).expenses, person.expenses)

    def test_run(self):
        person = self.person
        CashFlow(person).run('equal')
        CashFlow(person).run('normal')
        self.assertRaises(CashFlow(person).run(''))
