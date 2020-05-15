"""
Created on 2020/5/15 10:31
Author: Xinyu Guo
Email: xyguo@bu.edu
IDE: PyCharm
"""

import unittest
from financial_planner.entities.CollegeStudent import CollegeStudent

class TestCollegeFunding(unittest.TestCase):

    def test_Student(self):

        student_test = CollegeStudent()
        student_test.add_Income(4000, 'schlorship')
        student_test.add_Expense(2000, 'car')

        self.assertEqual(2000, student_test.annual_Expense)
        self.assertEqual(4000, student_test.annual_Income)
        self.assertEqual(-2000, student_test.annual_Net_Expense)


