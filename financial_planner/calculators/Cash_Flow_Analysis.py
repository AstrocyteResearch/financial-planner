import datetime
import pandas as pd
import numpy as np

class CashFlow(object):
    """
       Calculate daily total income, expense and net income
    """

    def __init__(self, person, periods=30*12*30, start_date=None):
        """
        Args:
            person
            periods
            start_date

        """
        self.person = person
        self.periods = periods
        self.start_date = start_date

        salary_growth_rate = person.salary_growth_rate
        income = person.income[0]
        expenses = person.expenses

        if start_date is None:
            today = datetime.datetime.today()
            if today.month == 12:
                start_date = datetime.datetime(today.year + 1, 1, 1)
            else:
                start_date = datetime.datetime(today.year, today.month + 1, 1)

        index = pd.period_range(start=start_date, periods=periods, freq='D')

        columns = ['income']
        for i in expenses:
            columns.append(i.name)
        columns.append('total expense')
        columns.append('net income')

        ts = pd.DataFrame(None, index=index, columns=columns, dtype=np.dtype("float"))

        # Set salary
        ts.loc[:, 'income'] = np.zeros(len(index))
        temp = 0
        for idx, row in ts.iterrows():
            if income.date != None:
                if idx.day == income.date:
                    row.loc['income'] = income.salary * (1 + salary_growth_rate) ** temp
                    temp +=1

        # Set expenses for each category
        for i in expenses:
            if i.date == None:
                ts.loc[:, i.name] = np.ones(len(index)) * i.amount / 30
            else:
                ts.loc[:, i.name] = np.zeros(len(index))
            for idx, row in ts.iterrows():
                if i.date != None:
                    if idx.day == i.date:
                        row.loc[i.name] = i.amount


        # Set total expense
        res = np.zeros(len(index))
        for i in expenses:
            res += ts.loc[:, i.name]
        ts.loc[:, 'total expense'] = res

        # Set net income
        ts.loc[:, 'net income'] = ts.loc[:, 'income'] - ts.loc[:, 'total expense']
        self.ts = ts

    def run(self):
        ts = self.ts
        return ts
