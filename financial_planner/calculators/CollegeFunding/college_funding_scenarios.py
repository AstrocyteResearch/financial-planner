"""
Created on 2020/5/12 16:31
Author: Xinyu Guo
Email: xyguo@bu.edu
IDE: PyCharm
"""
import pandas as pd
import numpy as np



class CollegeFundingScenario:
    def __init__(self, Student, ColType='in-state', State='Avg', CostIncrsRate=0.05,
                 investrate=0.04, Tax=0.25, yrs_to_col=10, balance=0, percent_saving=1.0, Name='Scenario1'):
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
        self.tuition = self.get_tuition()
        self.prv_tuition = 34740
        self.LivingExpense = {'Public': 10800, 'Private': 12000}
        self.BookExpense = 1200

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

    def cal_monthly_savings(self):
        Discounts = np.sum([1 /
                            (1 +
                             self.investrate * (1 - self.Tax) /
                             12)**t for t in range(1, (self.Student.period +
                                                       self.yrs_to_col) *
                                                   12)])
        savings = (self.TotalCost_PV * self.percent_saving -
                   self.balance) / Discounts
        return savings

    def run(self):
        AnnCost = []
        if self.ColType == 'Private':
            Anntuition = self.prv_tuition
            Annliving = self.LivingExpense['Private']
        else:
            Anntuition = self.tuition[self.State][self.ColType]
            Annliving = self.LivingExpense['Public']
        AnnCost.append(Anntuition)
        AnnCost.append(self.BookExpense)
        AnnCost.append(Annliving)
        AnnCost.append(self.Student.Annual_Net_Expense)
        TotalAnnCost = np.sum(AnnCost)

        period = self.Student.period
        r = self.investrate
        Cost_CF = [TotalAnnCost *
                   (1 +
                    r)**i for i in range(self.yrs_to_col, self.yrs_to_col +
                                         period +
                                         1)]
        self.TotalCost = np.sum(Cost_CF)
        self.TotalCost_PV = np.sum([
            CF * (1 + r)**(-i) for i, CF in enumerate(Cost_CF, start=self.yrs_to_col)])
        self.mon_savings = self.cal_monthly_savings()
        self.freshman_cost = Cost_CF[0]

        return {'name': self.Scenario_name,
                'values': {
                    'State': self.State,
                    'College Type': self.ColType,
                    'College Study Period': period,
                    'Current Tuition': Anntuition,
                    'Living Expense': Annliving,
                    'Books and Supplies Fee': self.BookExpense,
                    'Other Expense during college': self.Student.Annual_Expense,
                    'Other Income during college': self.Student.Annual_Income,
                    'Annual Net Cost': TotalAnnCost,
                    'Expected cost in Freshman year': self.freshman_cost,
                    'Total Cost for college': self.TotalCost,
                    'Total Cost in current money': self.TotalCost_PV,
                    'Percent of costs from savings': self.percent_saving,
                    'Equivalent monthly saving': self.mon_savings}
                }


if __name__ == '__main__':
    Student1 = CollegeStudent()
    Student1.add_Expense(2000, 'Play')
    Student1.add_Income(3000, 'Scholarship')

    scenario = CollegeFundingScenario(Student1, ColType='out-of-state', State='California', CostIncrsRate=0.05,
                                      investrate=0.04, Tax=0.25, yrs_to_col=6, balance=10000, percent_saving=0.8)
    result = scenario.run()
    df = pd.DataFrame.from_dict(
        result['values'],
        orient='index',
        columns=[
            result['name']])
    print(df)
