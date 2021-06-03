#!/usr/bin/env python
# coding: utf-8
'''
Description : calculator for how much life insurance is needed

@author : Jincheng Dan 
email   : jcdan@bu.edu
'''

import numpy as np
import pandas as pd



from financial_planner.entities.term_structure import term_structure



# get interest rate of US treasury
chromdriver_path = 'D:\\chromedriver\\chromedriver_win32\\chromedriver.exe'
term_struc = term_structure(chromdriver_path)



class Life_insurance():
    '''calculate the amount of life insurance a customer needs to purchase
    '''
    def __init__(self, annual_income, required_percentage, required_years, inflation_rate,
                 wage_growth_rate, one_time_expenses,term_structure = term_struc):
        '''current_annual_income is the current annual income amount of the customer.
           current_required_percentage is the minimum percentage of the customer's income 
           that is required by his dependents currently.
           required_years is how many years customer's dependents will need the income.
           inflation_rate is the expected rate of future inflation.
           wage_growth_rate is the expected rate of future wage growth.
           one_time_expenses is the expenses that will happen once, mainly, they are
           tuition, funeral cost, mortgage, other debt.
        '''
        self.current_annual_income = annual_income
        self.current_required_percentage = required_percentage
        self.required_years = required_years
        
        # allow inflation_rate input to be a constant or a list
        if type(inflation_rate) == float :
            self.inflation_rate = np.repeat(inflation_rate, required_years)
        elif len(inflation_rate) >= required_years :
            self.inflation_rate = np.array(inflation_rate[:required_years])
        else :
            raise Exception('Error: inflation rate should be a constant or match required years')
        
        self.wage_growth_rate = wage_growth_rate
        self.term_structure = term_structure
        self.one_time_expenses = one_time_expenses
   
    def discount_factor(self):
        nyears = self.required_years
        term_str = self.term_structure[:nyears]
        discount_f = [1/(1+term_str[i])**(i+1) for i in range(nyears)]
        return discount_f
    
    def inflation_factor(self):
        infl_factor = np.cumprod(1+self.inflation_rate)
        return infl_factor
    
    def minimum_insurance_amount(self):
        '''the minimum amount of insurance needed in order to fit the minimum needs of dependents in case
           some accidents happen tommorow .
           to keep the minimum living standard, the amount of income required in each future year
           should be adjusted by inflation
        '''
        current_min_required_amount = self.current_annual_income * self.current_required_percentage
        future_min_required_cashflow = current_min_required_amount * self.inflation_factor()
        present_value = sum(future_min_required_cashflow * self.discount_factor())
        min_required_amount = present_value + self.one_time_expenses
        print('The minimum amount of insurance needed in order to fit the minimum needs of dependents (in case some accidents happen tommorow) plus some one-time expenses is $%.2f. \n' % min_required_amount)
        return min_required_amount
    
    def perfect_replication_amount(self):
        '''the amount of insurance needed in order to replicate the future wage cashflow plus some
           one-time expenses. in this case wage grows follow the growth rate
        '''
        wage_cashflow = self.current_annual_income * np.array([(1+self.wage_growth_rate)**(n+1) for n in range(self.required_years)])
        present_value = sum(wage_cashflow * self.discount_factor())
        replication_amount = present_value + self.one_time_expenses
        print('The amount of insurance needed in order to fully replicate the future wage cashflow (in case some accidents happen tommorow) plus some one-time expenses is $%.2f. \n' %  replication_amount)
        return replication_amount
    
    def keep_current_living_standard_amount(self):
        '''the amount of insurance needed in order to keep current living standard. in this case cashflow
           is adjusted to inflation
        '''
        required_cashflow = self.current_annual_income * self.inflation_factor()
        present_value = sum(required_cashflow * self.discount_factor())
        required_amount = present_value + self.one_time_expenses
        print('The amount of insurance needed in order to keep current living standard (in case some accidents happen tommorow) plus some one-time expenses is %.2f. \n' % required_amount )
        return required_amount
    
    def result_display(self):
        self.minimum_insurance_amount()
        self.perfect_replication_amount()
        self.keep_current_living_standard_amount()

        



# test and example
if __name__ == '__main__':
    # input inflation rate is a constant
    L = Life_insurance(1000,0.5,10,0.01,0.02,0)
    print(L.discount_factor())
    print(L.inflation_factor())


    L.minimum_insurance_amount()
    L.perfect_replication_amount()
    L.keep_current_living_standard_amount()
    
    
    L.result_display()
    

    
    
    # input inflation rate is a list
    infl = [0.01, 0.02, 0.01, 0.01, 0.02, 0.011, 0.015, 0.014, 0.008, 0.007]
    L = Life_insurance(1000,0.5,10,infl,0.02,0)
    L.result_display()
    
    # rause exception
    L = Life_insurance(1000,0.5,10,[0.10,0.1],0.02,0)







