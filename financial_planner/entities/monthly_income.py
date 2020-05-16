from financial_planner.entities.income import Job


class MonthlyIncome(Job):
    """
       Define income that is received on a specific day in a month
    """

    def __init__(self, salary=50000, salary_growth_rate=0.01, savings_rate=0.05, date=None, name='income'):
        assert salary >= 0
        assert salary_growth_rate >= 0
        assert savings_rate >= 0
        assert isinstance(name, str)
        if date != None:
            assert isinstance(date, int)
            if date < 0 or date > 28:
                raise ValueError('date should be in range 0 to 28')
        Job.__init__(self, salary, salary_growth_rate, savings_rate)
        self.name = name
        self.date = date
