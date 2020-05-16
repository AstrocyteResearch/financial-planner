import unittest
import sys
sys.path.append('/Users/suyangshuang/Documents/GitHub/financial-planner/financial_planner/entities')
from mortgage_acceleration import mortgage

class TestMortgage(unittest.TestCase):
	"""Test mortgage_acceleration.py"""
	def setUp(self):
		self.mtg_1 = mortgage(9, 20, 200000, 1000, 0.12)
		self.mtg_2 = mortgage(1, 1, 200000, 1000, 0.12)
		self.mtg_3 = mortgage(9, 20, 10000, 10000, 0.12)

	def tearDown(self):
		pass

	def test_mortgage_saving_time(self):
		self.assertEqual(self.mtg_1.saving_time,47)
		self.assertEqual(self.mtg_2.saving_time,0)
		self.assertEqual(self.mtg_3.saving_time, 107)

	def test_mortgage_total_saving(self):
		self.assertEqual(self.mtg_1.total_saving, 43748)
		self.assertEqual(self.mtg_2.total_saving, 742)
		self.assertEqual(self.mtg_3.total_saving, 4640)
if __name__ == "__main__":
	unittest.main()
