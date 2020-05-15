class MonthlyExpenses(object):
    """
        Define expense that is paid on a specific day in a month, date=None means daily expense
    """

    def __init__(self, name, amount=0, date=None):
        assert isinstance(name, str)
        assert amount >= 0
        if date != None:
            assert isinstance(date, int)
            if date < 0 or date > 28:
                raise ValueError('date should be in range 0 to 28')
        self.name = name
        self.amount = amount
        self.date = date
