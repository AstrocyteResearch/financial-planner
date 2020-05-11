"""Person Class

"""
import numpy as np

class Household(object):

    def __init__(self):
        self.people = []

    def add_person(self, person):
        self.people.append(person)

    def to_dict(self):
        return {
            'people': self.people
        }


class Person(object):

    def __init__(self, name=None, age=None, gender=None):
        self.age = age
        self.gender = gender
        self.name = name
        self.income = []
        self.expenses = []

    def add_job(self, job):
        self.income.append(job)

    def add_expense(self, expense):
        self.expenses.append(expense)

    @property
    def salary(self):
        return np.sum([i.salary for i in self.income])

    @property
    def current_expenses(self):
        return np.sum([i.amount for i in self.expenses])

    @property
    def salary_growth_rate(self):
        # weighted average of all salaries
        total_salary = self.salary
        return np.sum([i.salary_growth_rate * i.salary / total_salary for i in self.income])

    @property
    def savings_rate(self):
        return 1 - self.current_expenses / self.salary

    def to_dict(self):
        return {
            'age': self.age,
            'gender': self.gender,
            'name': self.name
        }
