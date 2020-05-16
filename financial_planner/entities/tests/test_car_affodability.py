import unittest
import sys
sys.path.append('/Users/suyangshuang/Documents/GitHub/financial-planner/financial_planner/entities')
from car_affordability import car_affordability

class TestMortgage(unittest.TestCase):
	"""Test mortgage_acceleration.py"""
	def setUp(self):
		self.car_1 = car_affordability(0, 0, 0, 0, 0, 0)
		self.car_2 = car_affordability(10000, 50000, 20000, 0.047, 24)

	#(self, monthly_payment, down_payment, trade_in_value, interest_rate: float, term, sales_tax=0.075)
	def tearDown(self):
		pass

	def test_car_value(self):
		self.assertEqual(self.car_1.value(),0)
		self.assertEqual(self.car_2.value(),1660330)

if __name__ == "__main__":
	unittest.main()
