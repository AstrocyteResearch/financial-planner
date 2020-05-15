class MonthlyIncome(object):
    """
       Define income that is received on a specific day in a month
    """

    def __init__(self, salary=50000, salary_growth_rate=0.01, savings_rate=0.05, date=None):
        assert salary >= 0
        assert salary_growth_rate >= 0
        assert savings_rate >= 0
        if date != None:
            assert isinstance(date, int)
            if date < 0 or date > 28:
                raise ValueError('date should be in range 0 to 28')
        self.salary = salary
        self.salary_growth_rate = salary_growth_rate
        self.savings_rate = savings_rate
        self.date = date

