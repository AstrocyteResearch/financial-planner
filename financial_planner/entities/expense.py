"""Job Class

"""
import pandas as pd


class Expenses(object):

    def __init__(self, name, amount=0, as_of_date=None):
        self.name = name
        self.amount = amount
        if isinstance(as_of_date, str):
            as_of_date = pd.to_datetime(as_of_date)
        self.as_of_date = as_of_date
