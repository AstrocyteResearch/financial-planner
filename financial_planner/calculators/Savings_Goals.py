import datetime
import pandas as pd
import numpy as np
from sympy import *

class SavingsGoals(object):

    """
    Compute the minimum savings given long term savings goal
    """

    def __init__(self, person, savings_goal, rf, savings_growth_rate=0, periods=30*12, start_date=None):
        """
        Args:
            person
            savings_goal
            rf
            savings_growth_rate
            periods
            start_date

        """
        self.person = person
        self.savings_goal = savings_goal
        self.rf = rf
        self.savings_growth_rate = savings_growth_rate
        self.periods = periods
        self.start_date = start_date

        salary = person.salary
        salary_growth_rate = person.salary_growth_rate
        current_expenses = person.current_expenses

        if start_date is None:
            today = datetime.datetime.today()
            if today.month == 12:
                start_date = datetime.datetime(today.year + 1, 1, 1)
            else:
                start_date = datetime.datetime(today.year, today.month + 1, 1)

        index = pd.period_range(start=start_date, periods=periods, freq='M')

        columns = ['income', 'expense', 'net income']

        ts = pd.DataFrame(None, index=index, columns=columns, dtype=pd.np.float)

        #Set monthly savings growth rate
        self.savings_growth_rate_monthly = (1 + savings_growth_rate) ** (1. / 12.)

        #Set risk free rate
        self.rf_monthly = (1 + rf) ** (1. / 12.)

        # Set salary
        salary_growth_factor_monthly = (1 + salary_growth_rate) ** (1. / 12.)
        monthly_salary = salary / 12.
        ts.loc[:, 'income'] = (np.ones(len(index)) * salary_growth_factor_monthly).cumprod() * monthly_salary

        # Set total expense
        ts['expense'] = current_expenses / 12.

        # Set net income
        ts['net income'] = ts.loc[:, 'income'] - ts.loc[:, 'expense']
        self.ts = ts
        
    def run(self):
        savings_growth_rate_monthly = self.savings_growth_rate_monthly
        rf_monthly = self.rf_monthly
        periods = self.periods
        savings_goal = self.savings_goal
        ts = self.ts

        def func(x):
            x = x * (np.ones(periods) * savings_growth_rate_monthly).cumprod()
            res = np.sum(x * (np.ones(periods) * rf_monthly).cumprod()[::-1])
            return res

        x = Symbol('x')
        savings_monthly = solve(func(x) - savings_goal)
        savings = savings_monthly * (np.ones(periods) * savings_growth_rate_monthly).cumprod()
        if all(ts['net income'] >= savings):
            ts['minimum savings'] = savings
        else:
            print('The savings goal is too high!\nPlease reset the savings goal.')
            ts['minimum savings'] = np.zeros(periods)
        return ts