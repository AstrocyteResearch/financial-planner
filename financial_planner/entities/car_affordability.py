class car_affordability():
	"Reference: https://www.cars.com/car-affordability-calculator/"

	def __init__(self, monthly_payment, down_payment, trade_in_value, interest_rate: float, term, sales_tax=0.075):
		"""
				Args:
					monthly_payment:
					down_payment:
					trade_in_value:
					sales_tax: float
					interest_rate: annually
					term: yearly
		"""
		self.monthly_payment = monthly_payment
		self.down_payment = down_payment
		self.trade_in_value = trade_in_value
		self.interest_rate = interest_rate
		self.term = term
		self.sales_tax = sales_tax

	def value(self):
		if self.interest_rate != 0:
			discounting_factor = 1 / (1 + self.interest_rate / 12)
			value = self.down_payment + self.trade_in_value + self.monthly_payment * discounting_factor * (1 - discounting_factor ** (self.term * 12)) / (1 - discounting_factor)
		else:
			value = self.down_payment + self.trade_in_value + self.monthly_payment * self.term * 12
		value -= value * self.sales_tax
		return round(value)

if __name__ == "__main__":
	car_1 = car_affordability(0,0,0,0,0,0)
	print(car_1.value())
	car_2 = car_affordability(10000, 50000, 20000, 0.047, 2)
	print(car_2.value())
	car_3 = car_affordability(10000, 50000, 20000, 0.047, 24)
	print(car_3.value())



