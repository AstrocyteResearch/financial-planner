#!/usr/bin/env python
# coding: utf-8
'''
Description : calculator for LTCI Cost of Waiting 

@author : Jincheng Dan 
email   : jcdan@bu.edu
'''

import numpy as np
import pandas as pd
from scipy.optimize import minimize       


from financial_planner.entities.term_structure import term_structure



# get interest rate of US treasury
chromdriver_path = 'D:\\chromedriver\\chromedriver_win32\\chromedriver.exe'
term_struc = term_structure(chromdriver_path)



class LTCI_cost_of_waiting():
    '''Calculate the Potential Cost of Waiting to Purchase a Long-Term-Care Insurance Policy
    '''
    def __init__(self,current_age, purchase_age, benifit_age, current_premium, future_premium,term_stru = term_struc):
        '''
        current_age, is the age current age of the customer.
        purchase_age, is the ages the customer plan to enter a insurance policy.
        benifit_age, is the age the customer will receive the benifit from the insurance.
        current_premium, is the annual premium if the customer enters the insurance right now.
        future_premium, is the annual premium if the customer enters the insurance at the purchase_age.
        chromdriver_path, is the local path for chromedriver which will be used in crawler.
        term_stru, is the term structure of US treasury.
        '''
        self.current_age = current_age
        self.purchase_age = purchase_age
        self.benifit_age = benifit_age
        self.current_premium = current_premium
        self.future_premium = future_premium
        self.term_structure = term_stru
        
    def discount_factor(self):
        nyears = self.benifit_age-self.current_age
        term_str = self.term_structure[:nyears]
        discount_f = [1] + [1/(1+term_str[i])**(i+1) for i in range(nyears-1)]
        return discount_f
        
    def future_cashflow(self):
        fut_cashflow = np.concatenate((np.zeros(self.purchase_age-self.current_age),
                                     np.repeat(self.future_premium,(self.benifit_age-self.purchase_age))))
        return fut_cashflow
        
    def current_cashflow(self):
        cur_cashflow = np.repeat(self.current_premium,(self.benifit_age-self.current_age))
        return cur_cashflow
    
    def cost_future_purchase(self):
        cost_fut_purchase = sum(self.discount_factor()*self.future_cashflow())
        return cost_fut_purchase
   
    def cost_current_purchase(self):
        cost_cur_purchase = sum(self.discount_factor()*self.current_cashflow())
        return cost_cur_purchase
    
    def potential_cost_of_waiting(self):
        waiting_cost = self.cost_future_purchase()-self.cost_current_purchase()
        print('The LTCI Cost of Waiting is $%f' % waiting_cost)
        return waiting_cost
    
    def potential_cost_of_waiting_opt(self):
        '''this function is used to do the optimization, we delet the print commend
        '''
        waiting_cost = self.cost_future_purchase()-self.cost_current_purchase()
        return waiting_cost
    
    def break_even_future_price(self):
        input_fu_premiun = self.future_premium
        def costfun(fu_premium):
            self.future_premium = fu_premium
            return self.potential_cost_of_waiting_opt()**2
        opt = minimize(costfun,self.current_premium)
        break_even_price = opt.x[0]
        self.future_premium = input_fu_premiun # restore the original future premium value
        print('If the future premium is %.2f it is the same purchasing the insurance right now or in               the future.' % break_even_price)
        return break_even_price




# test and example
if __name__ == '__main__':
    L = LTCI_cost_of_waiting(55,56,80,1480,1598,term_struc)
    print(L.current_cashflow())
    print(L.future_cashflow())
    print(L.cost_current_purchase())
    print(L.cost_future_purchase())
    L.potential_cost_of_waiting()
    L.break_even_future_price()
    print(L.future_premium)
    print(L.future_cashflow())





