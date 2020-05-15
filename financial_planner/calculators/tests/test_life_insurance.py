# -*- coding: utf-8 -*-
"""
Discreption : test of the life_insurance calculator
Created on Thu May 14 23:26:05 2020

@author : Jincheng Dan 
email   : jcdan@bu.edu
"""

import unittest
from financial_planner.calculators.credit.life_insurance import Life_insurance

class Life_Insurance_Test_Case(unittest.TestCase):
    
    def setUp(self):
        self.life_insurance_1 = life_insurance.Life_insurance(1000, 0.5, 2, 0.01, 0.01, 3000, [0,0.01])
        self.life_insurance_2 = life_insurance.Life_insurance(1000, 1, 2, [0.005,0.01], 0.005, 3000, [0.01,0.01])
        
    def tearDown(self):
        pass
    
    def test_inflation_rate(self):
        for i in range(len(self.life_insurance_1.inflation_factor())):
            self.assertEqual(self.life_insurance_1.inflation_factor()[i],
                             [(1+0.01),(1+0.01)**2][i])
            self.assertEqual(self.life_insurance_2.inflation_factor()[i],
                             [(1+0.005),(1+0.005)*(1+0.01)][i])

    def test_discount_factor(self):
        for i in range(len(self.life_insurance_1.inflation_factor())):
            self.assertEqual(self.life_insurance_1.discount_factor()[i],
                             [1/(1+0),1/((1+0.01)**2)][i])
            self.assertEqual(self.life_insurance_2.discount_factor()[i],
                             [1/(1+0.01),1/((1+0.01)*(1+0.01))][i])
    
    def test_perfect_replication_amount(self):
        self.assertEqual(self.life_insurance_1.perfect_replication_amount(),
                         (1000*(1+0.01)/(1+0) +  1000*(1+0.01)**2/(1+0.01)**2 + 3000))
        self.assertEqual(self.life_insurance_2.perfect_replication_amount(),
                         (1000*(1+0.005)/(1+0.01) +  1000*(1+0.005)**2/(1+0.01)**2 + 3000))
        
    def test_keep_current_living_standard_amount(self):
        self.assertEqual(self.life_insurance_1.keep_current_living_standard_amount(),
                         (1000*(1+0.01)/(1+0) +  1000*(1+0.01)**2/(1+0.01)**2 + 3000))
        self.assertEqual(self.life_insurance_2.keep_current_living_standard_amount(),
                         (1000*(1+0.005)/(1+0.01) +  1000*(1+0.005)*(1+0.01)/(1+0.01)**2 + 3000))
        
    def test_minimum_insurance_amount(self):
        self.assertEqual(self.life_insurance_1.minimum_insurance_amount(),
                         (1000*0.5*(1+0.01)/(1+0) +  1000*0.5*(1+0.01)**2/(1+0.01)**2 + 3000))
        self.assertEqual(self.life_insurance_2.minimum_insurance_amount(),
                         (1000*(1+0.005)/(1+0.01) +  1000*(1+0.005)*(1+0.01)/(1+0.01)**2 + 3000))
        
        
        
if __name__ == '__main__':
    unittest.main()
