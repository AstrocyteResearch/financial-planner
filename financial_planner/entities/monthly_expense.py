class MonthlyExpenses(object):
    """
        Define expense that is paid on a specific day in a month, date=None means daily expense
    """

    def __init__(self, name, amount=0, date=None):
        self.name = name
        self.amount = amount
        self.date = date
