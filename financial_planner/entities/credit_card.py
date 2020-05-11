"""Optimal credit card payment calculator

Show that the optimal prepayment for a set of credit cards with monthly payments is

For a given credit card you have a :
    * B_it - balance from card i at time t
    * r_it - annual interest rate for card i at time t
    * m_it - minimum monthly payment of card i at time t

Variables exogenous to credit card debt
    * S_t - annual salary at time t
    * d_t - discount rate at time t (annualized)

You can try to minimize these things
 * Total amount paid
 * NPV of total debt paid
 * Time to debt-free


# TODO handle different aprs for a single card:
    If your account has balances with different APRs, payments in excess of the Minimum Payment Due are applied to
    Interest Charges and other fees and to balances with the highest APRs, before being applied to balances
    with lowest APRs. The structure is opposite for the application of the Minimum Payment; this means that
    balances with higher APRs are not reduced until balances with lower APRs have been paid off.
"""
import numpy as np
from operator import itemgetter
import datetime


class CreditCard(object):
    """has APR"""

    def __init__(self, aprs=None, balances=None, balance_types=None, monthly_due_day=1, credit_limit=1e6, name="Credit Card",
                 account_number=None, min_interest_charge=1., min_payment_rate=0.02, late_fee=25.):
        """

        Args:
            aprs:
            balances:
            balance_types:
            monthly_due_day:
            credit_limit:
            name:
            account_number:
            min_interest_charge:
            min_payment_rate:
            late_fee:
        """

        assert aprs is not None, "aprs must be defined"

        if isinstance(aprs, (float, np.float, np.float64)):
            aprs = [aprs]
        if balances is not None:
            assert len(balances) == len(aprs), "balances must be the same length as aprs"
        else:
            balances = np.zeros(len(aprs))
        if balance_types is not None:
            assert len(balance_types) == len(aprs), "balance types must be the same length as aprs"
        else:
            balance_types = ['balance_{}'.format(i) for i in range(len(aprs))]

        # Sort APRS from lowest to highest amounts to facilitate paydowns
        aprs, balances, balance_types = zip(
            *sorted(zip(aprs, balances, balance_types), key=itemgetter(0), reverse=False)
        )

        self.aprs = np.array(aprs)
        self.balances = np.array(balances)
        self.balance_types = balance_types

        # Other credit card amounts
        self.monthly_due_day = monthly_due_day
        self.credit_limit = credit_limit
        self.name = name
        self.account_number = account_number
        self.min_interest_charge = min_interest_charge
        self.min_payment_rate = min_payment_rate
        self.late_fee = late_fee

    def to_dict(self):
        return {
            'monthly_due_day': self.monthly_due_day,
            'credit_limit': self.credit_limit,
            'name': self.name,
            'account_number': self.account_number,
            'min_interest_charge': self.min_interest_charge,
            'min_payment_rate': self.min_payment_rate,
            'aprs': self.aprs.tolist(),
            'balances': self.balances.tolist(),
            'balance_types': self.balance_types,
            'late_fee': self.late_fee
        }

    def copy(self):
        return self.loads(self.dumps())

    def dumps(self):
        """"""
        import json
        return json.dumps(self.to_dict())

    @staticmethod
    def loads(s):
        import json
        obj = json.loads(s)
        return CreditCard(**obj)

    def __str__(self):
        import pprint
        return 'CreditCard:\n{}'.format(pprint.pformat(self.to_dict(), indent=4))

    def hypothetical_interest_given_payment(self, payment_amount, avg_daily_balance=None):
        """Has no sideeffects to balances

        Args:
            amount:
            avg_daily_balance:

        Returns:

        """
        orig_balances = self.balances.copy()
        self.paydown(payment_amount, avg_daily_balance=avg_daily_balance)
        int_charges = self.calc_interest_charge(avg_daily_balance=avg_daily_balance)
        self.balances = orig_balances
        return int_charges.sum()

    def advance_month(self, payment_amount=0.0, avg_daily_balance=None):
        """

        Args:
            payment_amount:
            avg_daily_balance:

        Returns:

        """
        interest_charges = self.calc_interest_charge().sum()
        self.charge(interest_charges)
        return self.paydown(payment_amount, avg_daily_balance=avg_daily_balance)

    def charge(self, amount):
        """Add to the highest balance

        Args:
            amount:

        Returns:

        """
        self.balances[-1] += amount

    def charge_late_fee(self):
        self.balances[-1] += self.late_fee
        return self.late_fee

    def paydown(self, amount, avg_daily_balance=None):
        """Reduce the balances for the minimum rate first

        Args:
            amount:

        Returns:

        """
        full_balance = self.balances.sum()

        if avg_daily_balance is None:
            avg_daily_balance = full_balance

        min_payment = self.calc_min_payments(avg_daily_balance)

        pay_towards_lowest_apr = max(0.0, min(amount, min_payment))
        pay_towards_highest_apr = max(0.0, amount - pay_towards_lowest_apr)

        # Paydown minimum amounts
        min_payment_acct_mask = (self.balances.cumsum() - pay_towards_lowest_apr) <= 0
        self.balances[min_payment_acct_mask] = 0.0
        partial_payment_acct = int((1*min_payment_acct_mask).sum())
        if 0 <= partial_payment_acct < len(self.balances):
            self.balances[partial_payment_acct] -= pay_towards_lowest_apr - (full_balance - self.balances.sum())

        # Paydown minimum amounts
        tmp_balance = self.balances.sum()
        max_payment_acct_mask = (self.balances[::-1].cumsum()[::-1] - pay_towards_highest_apr) <= 0
        self.balances[max_payment_acct_mask] = 0.0
        partial_payment_acct = len(self.balances) - int((1 * max_payment_acct_mask).sum()) - 1
        if 0 <= partial_payment_acct < len(self.balances):
            self.balances[partial_payment_acct] -= min(self.balances[partial_payment_acct], pay_towards_highest_apr - (tmp_balance - self.balances.sum()))

        # Rounding adjustment
        self.balances = np.round(self.balances, 2)
        remaining_amount = np.round(amount - (full_balance - self.balances.sum()))
        return remaining_amount

    def calc_interest_charge(self, avg_daily_balance=None, date=None):
        """Assumes Actual / 365 APR conventions

        Args:
            avg_daily_balance: np.array

        Returns:

        """
        if avg_daily_balance is None:
            avg_daily_balance = self.balances
        year_frac = float((self.next_due_date(date=date) - self.prev_due_date(date=date)).days) / 365.
        return np.round(self.aprs * avg_daily_balance * year_frac, 2)

    def calc_min_payments(self, avg_daily_balance=None):
        """Assumes Actual / 365 APR conventions

        Args:
            avg_daily_balance: np.array

        Returns:

        """
        if avg_daily_balance is None:
            avg_daily_balance = self.balances
        return np.round(np.sum(avg_daily_balance) * self.min_payment_rate, 2)

    def next_due_date(self, date=None):
        if date is None:
            date = datetime.datetime.today()

        if date.day <= self.monthly_due_day:
            return datetime.datetime(date.year, date.month, self.monthly_due_day)
        else:
            if date.month == 12:
                return datetime.datetime(date.year + 1, 1, self.monthly_due_day)
            else:
                return datetime.datetime(date.year, date.month + 1, self.monthly_due_day)

    def prev_due_date(self, date=None):

        prev_date = self.next_due_date(date=date)
        if prev_date.month == 1:
            return datetime.datetime(prev_date.year - 1, 12, prev_date.day)
        else:
            return datetime.datetime(prev_date.year, prev_date.month - 1, prev_date.day)

