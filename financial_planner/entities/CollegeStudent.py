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
        self.ann_Expense = {}
        self.ann_Income = {}

    def add_Expense(self, Expense, genre):
        self.ann_Expense[genre] = Expense

    def add_Income(self, Income, genre):
        self.ann_Income[genre] = Income

    @property
    def annual_Expense(self):
        return np.sum([amount for amount in self.ann_Expense.values()])

    @property
    def annual_Income(self):
        return np.sum([amount for amount in self.ann_Income.values()])

    @property
    def annual_Net_Expense(self):
        return self.annual_Expense - self.annual_Income
