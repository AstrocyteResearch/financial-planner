# Author: Yangshuang Su
# May 14 2020
import pandas as pd
import numpy as np


class mortgage():
	"Reference: https://www.bankrate.com/calculators/mortgages/mortgage-loan-payoff-calculator.aspx"

	def __init__(self, years_remaining, oringinal_mortgage_term, oringinal_mortgage_amount, additional_payment,
				interest_rate: float):
		"""
			Args:
				years_remaining:
				oringinal_mortgage_term:
				oringinal_mortgage_amount:
				additional_payment:
				interest_rate: annually
		"""
		assert years_remaining <= oringinal_mortgage_term, 'years remaing has to be less than oringinal_mortgage_term'
		assert interest_rate <= 1
		self.years_remaining = years_remaining
		self.oringinal_mortgage_term = oringinal_mortgage_term
		self.oringinal_mortgage_amount = oringinal_mortgage_amount
		self.additional_payment = additional_payment
		self.interest_rate = interest_rate

	def run(self):
		"""run the algorithm"""
		# build array
		balance = np.zeros(self.oringinal_mortgage_term * 12 + 1) - 1
		payment = np.zeros(self.oringinal_mortgage_term * 12)
		interest = np.zeros(self.oringinal_mortgage_term * 12)
		oringinal_payment = np.zeros(self.oringinal_mortgage_term * 12)

		# lambda
		discounting_factor = 1 / (1 + self.interest_rate / 12)
		normal_payment = self.oringinal_mortgage_amount * (1 - discounting_factor) / (
				discounting_factor * (1 - discounting_factor ** (self.oringinal_mortgage_term * 12)))

		# Initialization
		balance[0] = self.oringinal_mortgage_amount
		oringinal_payment += normal_payment
		payment += normal_payment
		payment[(self.oringinal_mortgage_term - self.years_remaining) * 12:] += self.additional_payment

		# update
		for i, _ in enumerate(payment):
			if balance[i] > 0:
				interest[i] = balance[i] * self.interest_rate / 12
				if balance[i] - (payment[i] - interest[i]) > 0:
					balance[i + 1] = balance[i] - (payment[i] - interest[i])
				else:
					balance[i + 1] = 0
					payment[i] = balance[i]
			else:
				payment[i] = 0

		# Dataframe
		df = pd.DataFrame()
		df['Payment'] = payment
		df['Interest'] = interest
		df['Balance'] = balance[1:]
		df['Original_payment'] = oringinal_payment

		filt = df['Balance'] >= 0
		report = df.loc[filt]
		print(report)

		return df

	@property
	def total_saving(self):
		df = self.run()
		total_saving = int(df['Original_payment'].sum() - df['Payment'].sum())
		return total_saving

	@property
	def saving_time(self):
		df = self.run()
		filt = df['Balance'] >= 0
		report = df.loc[filt]
		saving_time = len(df) - len(report)
		return saving_time


if __name__ == "__main__":
	mtg_1 = mortgage(9, 20, 200000, 1000, 0.12)
	print('saving_time:{}\ntotal_saving:{}'.format(mtg_1.saving_time, mtg_1.total_saving))
	mtg_2 = mortgage(1, 1, 200000, 1000, 0.12)
	print('saving_time:{}\ntotal_saving:{}'.format(mtg_2.saving_time, mtg_2.total_saving))
	mtg_3 = mortgage(9, 20, 10000, 10000, 0.12)
	print('saving_time:{}\ntotal_saving:{}'.format(mtg_3.saving_time, mtg_3.total_saving))
