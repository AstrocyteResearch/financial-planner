"""Job Class

"""


class Job(object):

    def __init__(self, salary=50000, salary_growth_rate=0.01, savings_rate=0.05):
        self.salary = salary
        self.salary_growth_rate = salary_growth_rate
        self.savings_rate = savings_rate

    def to_dict(self):
        return {
            'salary': self.salary,
            'salary_growth_rate': self.salary_growth_rate,
            'savings_rate': self.savings_rate
        }
