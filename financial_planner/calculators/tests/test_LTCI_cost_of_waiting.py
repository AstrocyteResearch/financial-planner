# -*- coding: utf-8 -*-
"""
Discreption : test of the LTCI_cost_of_waiting calculator
Created on Thu May 14 23:26:10 2020

@author : Jincheng Dan 
email   : jcdan@bu.edu
"""

import unittest
from financial_planner.calculators.LTCI_cost_of_waiting import LTCI_cost_of_waiting


class LTCI_cost_of_waiting_Test_Case(unittest.TestCase):
    
    def setUp(self):
        self.LTCI_cost_of_waiting_1 = LTCI_cost_of_waiting.LTCI_cost_of_waiting(50, 51, 52, 1000, 2100, [0,0.01])
        self.LTCI_cost_of_waiting_2 = LTCI_cost_of_waiting.LTCI_cost_of_waiting(50, 51, 52, 1000, 1500, [0.01,0.01])
        
    def tearDown(self):
        pass
    
    def test_discount_factor(self):
        for i in range(self.LTCI_cost_of_waiting_1.benifit_age-self.LTCI_cost_of_waiting_1.current_age):
            self.assertEqual(self.LTCI_cost_of_waiting_1.discount_factor(),[1/(1)**0,1/(1+0)**1])
        for i in range(self.LTCI_cost_of_waiting_2.benifit_age-self.LTCI_cost_of_waiting_2.current_age):
            self.assertEqual(self.LTCI_cost_of_waiting_2.discount_factor(),[1/(1)**0,1/(1+0.01)**1])
    
    def test_future_cashflow(self):
        for i in range(self.LTCI_cost_of_waiting_1.benifit_age-self.LTCI_cost_of_waiting_1.current_age):
            self.assertEqual(self.LTCI_cost_of_waiting_1.future_cashflow()[i],[0,2100][i])
        for i in range(self.LTCI_cost_of_waiting_2.benifit_age-self.LTCI_cost_of_waiting_2.current_age):
            self.assertEqual(self.LTCI_cost_of_waiting_2.future_cashflow()[i],[0,1500][i])
            
    def test_current_cashflow(self):
        for i in range(self.LTCI_cost_of_waiting_1.benifit_age-self.LTCI_cost_of_waiting_1.current_age):
            self.assertEqual(self.LTCI_cost_of_waiting_1.current_cashflow()[i],[1000,1000][i])
        for i in range(self.LTCI_cost_of_waiting_2.benifit_age-self.LTCI_cost_of_waiting_2.current_age):
            self.assertEqual(self.LTCI_cost_of_waiting_2.current_cashflow()[i],[1000,1000][i])
   
    def test_cost_future_purchase(self):
        self.assertEqual(self.LTCI_cost_of_waiting_1.cost_future_purchase(),(2100/1))
        self.assertEqual(self.LTCI_cost_of_waiting_2.cost_future_purchase(),(1500/(1+0.01)))

    def test_cost_current_purchase(self):
        self.assertEqual(self.LTCI_cost_of_waiting_1.cost_current_purchase(),(1000/1+1000/1))
        self.assertEqual(self.LTCI_cost_of_waiting_2.cost_current_purchase(),(1000/1+1000/(1+0.01)))

    def test_potential_cost_of_waiting(self):
        self.assertEqual(self.LTCI_cost_of_waiting_1.potential_cost_of_waiting(),(2100/1-(1000/1+1000/1)))
        self.assertEqual(self.LTCI_cost_of_waiting_2.potential_cost_of_waiting(),(1500/(1+0.01)-(1000/1+1000/(1+0.01))))

    def test_break_even_future_price(self):
        self.assertEqual(round(self.LTCI_cost_of_waiting_1.break_even_future_price()/1-
                         self.LTCI_cost_of_waiting_1.cost_current_purchase()),0)
        self.assertEqual(round(self.LTCI_cost_of_waiting_2.break_even_future_price()/(1+0.01)-
                         self.LTCI_cost_of_waiting_2.cost_current_purchase()),0)


if __name__ == '__main__':
    unittest.main()
