"""
Created on 2020/5/12 16:31
Author: Xinyu Guo
Email: xyguo@bu.edu
IDE: PyCharm
"""
import pandas as pd
import numpy as np


class Tuition:
    def __init__(self):
        '''
        Return:
            The tuition dictionary for different states and college types
        '''
        self.tuition = self.get_tuition()

    def get_tuition(self):
        df = pd.read_csv('Tuition.csv')
        df.set_index('State', inplace=True)
        df.columns = ['in-state', 'out-of-state']
        tuition = df.T.to_dict()

        # average tuition of in-state and out-state
        tuition['Avg'] = {
            'in-state': df.mean()[0],
            'out-of-state': df.mean()[1]}
        return tuition

class CollegeFundingScenario:
    def __init__(self, Student, ColType='in-state', State='Avg', CostIncrsRate=0.05,
                 investrate=0.04, Tax=0.25, yrs_to_col=10, balance=0, percent_saving=1.0, Name='Scenario1'):
        '''
        Args:
            Student: CollegeStudent Object

            ColType: str, {'in-state', 'out-of-state', 'private'}

            State: str, {state name, 'Avg'}

            CostIncrsRate: float
                Annual increase rate of college cost

            investrate: float
                Investment rate for the savings account, also used as discount rate

            Tax: float
                Tax rate imposed on the interest income

            yrs_to_col: int
                The remaining years to the start of the college

            balance: int
                Current balance of the savings account

            percent_saving: float
                The percent of the college cost that would be paid by the savings account

            Name: str
                Scenario Name

        Return:
            A dict containing the result of the calculation
        '''
        self.Scenario_name = Name
        self.Student = Student
        self.ColType = ColType
        self.State = State
        self.CostIncrsRate = CostIncrsRate
        self.investrate = investrate
        self.Tax = Tax
        self.yrs_to_col = yrs_to_col
        self.balance = balance
        self.percent_saving = percent_saving
        self.tuition = Tuition().tuition
        self.prv_tuition = 34740
        self.LivingExpense = {'Public': 10800, 'Private': 12000}
        self.bookExpense = 1200

    def cal_monthly_savings(self):
        Discounts = np.sum([1 / (1 + self.investrate * (1 - self.Tax) /
                             12)**t for t in range(1, (self.Student.period +
                                                       self.yrs_to_col) * 12)])
        savings = (self.totalCost_PV * self.percent_saving -
                   self.balance) / Discounts
        return savings

    def run(self):
        AnnCost = []
        if self.ColType == 'Private':
            anntuition = self.prv_tuition
            annliving = self.LivingExpense['Private']
        else:
            anntuition = self.tuition[self.State][self.ColType]
            annliving = self.LivingExpense['Public']
        AnnCost.append(anntuition)
        AnnCost.append(self.bookExpense)
        AnnCost.append(annliving)
        AnnCost.append(self.Student.annual_Net_Expense)
        totalAnnCost = np.sum(AnnCost)

        period = self.Student.period
        r = self.investrate
        cost_CF = [totalAnnCost *
                   (1 + r)**i for i in range(self.yrs_to_col, self.yrs_to_col +
                                         period + 1)]
        self.totalCost = np.sum(cost_CF)
        self.totalCost_PV = np.sum([
            CF * (1 + r)**(-i) for i, CF in enumerate(cost_CF, start=self.yrs_to_col)])
        self.mon_savings = self.cal_monthly_savings()
        self.freshman_cost = cost_CF[0]

        return {'name': self.Scenario_name,
                'values': {
                    'State': self.State,
                    'College Type': self.ColType,
                    'College Study Period': period,
                    'Current Tuition': anntuition,
                    'Living Expense': annliving,
                    'Books and Supplies Fee': self.bookExpense,
                    'Other Expense during college': self.Student.annual_Expense,
                    'Other Income during college': self.Student.annual_Income,
                    'Annual Net Cost': totalAnnCost,
                    'Expected cost in Freshman year': self.freshman_cost,
                    'Total Cost for college': self.totalCost,
                    'Total Cost in current money': self.totalCost_PV,
                    'Percent of costs from savings': self.percent_saving,
                    'Equivalent monthly saving': self.mon_savings}
                }


