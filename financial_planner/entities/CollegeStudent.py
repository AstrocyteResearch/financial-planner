"""
Created on 2020/5/13 14:54
Author: Xinyu Guo
Email: xyguo@bu.edu
IDE: PyCharm
"""
import numpy as np

class CollegeStudent:
    def __init__(self, study_period=4, name=None, age=None, gender=None):
        self.period = study_period
        self.age = age
        self.gender = gender
        self.name = name
        self.Ann_Expense = {}
        self.Ann_Income = {}

    def add_Expense(self, Expense, genre):
        self.Ann_Expense[genre] = Expense

    def add_Income(self, Income, genre):
        self.Ann_Income[genre] = Income

    @property
    def Annual_Expense(self):
        return np.sum([amount for amount in self.Ann_Expense.values()])

    @property
    def Annual_Income(self):
        return np.sum([amount for amount in self.Ann_Income.values()])

    @property
    def Annual_Net_Expense(self):
        return self.Annual_Expense - self.Annual_Income
