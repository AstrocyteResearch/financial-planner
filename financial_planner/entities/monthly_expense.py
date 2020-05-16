from financial_planner.entities.expense import Expenses


class MonthlyExpenses(Expenses):
    """
        Define expense that is paid on a specific day in a month
    """

    def __init__(self, name='expense', amount=0, as_of_date=None, date=None):
        assert isinstance(name, str)
        assert amount >= 0
        if date != None:
            assert isinstance(date, int)
            if date < 0 or date > 28:
                raise ValueError('date should be in range 0 to 28')
        Expenses.__init__(self, name, amount, as_of_date)
        self.date = date
