import datetime
import pandas as pd
import numpy as np
from financial_planner.entities.monthly_expense import MonthlyExpenses
from financial_planner.entities.monthly_income import MonthlyIncome


class CashFlow(object):
    """
       Calculate daily total income, expense and net income
    """

    def __init__(self, person, periods=30 * 12 * 30, start_date=None):
        """
        Args:
            person
            periods
            start_date

        """
        self.person = person
        self.periods = periods
        self.start_date = start_date
        self.salary_growth_rate = person.salary_growth_rate
        self.income = person.income[0]
        self.expenses = person.expenses

        if start_date is None:
            today = datetime.datetime.today()
            if today.month == 12:
                start_date = datetime.datetime(today.year + 1, 1, 1)
            else:
                start_date = datetime.datetime(today.year, today.month + 1, 1)
        self.start_date = start_date

    def run(self, scenario_name='equal'):
        """
           scenario_name defines how the daily expenses distribute: 'equal' or 'normal'
           equal means the daily expenses is the same
           normal means the daily expenses follow a normal distribution
        """
        person = self.person
        periods = self.periods
        start_date = self.start_date
        salary_growth_rate = self.salary_growth_rate
        income = self.income
        expenses = self.expenses

        index = pd.period_range(start=start_date, periods=periods, freq='D')

        columns = ['income']
        for i in expenses:
            columns.append(i.name)
        columns.append('total expense')
        columns.append('net income')

        ts = pd.DataFrame(None, index=index, columns=columns, dtype=np.dtype("float"))

        # Set income
        ts.loc[:, 'income'] = np.zeros(len(index))
        temp = 0
        for idx, row in ts.iterrows():
            if income.date != None:
                if idx.day == income.date:
                    row.loc['income'] = income.salary * (1 + salary_growth_rate) ** temp
                    temp += 1

        # Set expenses for each category
        for i in expenses:
            if isinstance(i, MonthlyExpenses):
                ts.loc[:, i.name] = np.zeros(len(index))
                temp = [j.day == i.date for j in ts.index]
                ts.loc[temp, i.name] = i.amount
            elif scenario_name == 'equal':
                ts.loc[:, i.name] = np.ones(len(index)) * i.amount / 30
            elif scenario_name == 'normal':
                mu = np.ones(len(index)) * i.amount / 30
                sigma = mu / 10
                ts.loc[:, i.name] = np.random.normal(mu, sigma, periods)
            else:
                raise ValueError('No such scenario!')

        # Set total expense
        names = [i.name for i in expenses]
        res = ts.loc[:, names].sum(axis=1)
        ts.loc[:, 'total expense'] = res

        # Set net income
        ts.loc[:, 'net income'] = ts.loc[:, 'income'] - ts.loc[:, 'total expense']
        self.ts = ts
        return ts
