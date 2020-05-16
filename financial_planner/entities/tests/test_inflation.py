"""
Created on 2020/5/15 16:30
Author: Xinyu Guo
Email: xyguo@bu.edu
IDE: PyCharm
"""


from financial_planner.calculators.PersonalInflation.personal_inflation_scenario import *
import unittest


class TestInflation(unittest.TestCase):

    def test_result(self):
        expense = {'food': 4500,
                   'education': 845,
                   'recreation': 750,
                   'medical': 890,
                   'transportation': 1125,
                   'apparel': 370,
                   'housing': 5110,
                   'other': 2510}

        Scenario1 = PersonalInflationScenario(expense)
        df = Scenario1.run()

        self.assertAlmostEqual(0.2795, df['Personal_weights']['Food'], places=3)
        self.assertAlmostEqual(0.0525, df['Personal_weights']['Education'], places=3)
        self.assertAlmostEqual(0.0466, df['Personal_weights']['Recreation'], places=3)
        self.assertAlmostEqual(0.0553, df['Personal_weights']['Medical'], places=3)
        self.assertAlmostEqual(0.0699, df['Personal_weights']['Transportation'], places=3)

