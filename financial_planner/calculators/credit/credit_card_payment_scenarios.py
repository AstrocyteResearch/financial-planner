import datetime
import pandas as pd
import numpy as np
import tqdm


class CreditCardScenario(object):

    def __init__(self, person, scenario_name=None, periods=30*12, start_date=None, discount_rate=0.02):
        """Return a dataframe configured with all exogenous variables

        Args:
            person:
            scenario_name: str
            periods:
            start_date:
            discount_rate:

        Returns:

        """
        self.person = person
        self.scenario_name = scenario_name
        self.periods = periods
        self.start_date = start_date
        self.discount_rate = discount_rate

        salary = person.salary
        salary_growth_rate = person.salary_growth_rate
        savings_rate = person.savings_rate

        if start_date is None:
            today = datetime.datetime.today()
            if today.month == 12:
                start_date = datetime.datetime(today.year + 1, 1, 1)
            else:
                start_date = datetime.datetime(today.year, today.month + 1, 1)

        index = pd.period_range(start=start_date, periods=periods, freq='M')

        columns = [
            'ref_period',
            'salary',
            'discount_factor',
            'gross_savings',
            'total_cc_balance',
            'interest_expense',
            'cc_payment',
            'avg_apr',
            'missed_payments',
            'late_fees'
        ]

        ts = pd.DataFrame(None, index=index, columns=columns, dtype=pd.np.float)
        ts.loc[:, 'ref_period'] = [str(dt) for dt in ts.index]

        # Set salary
        salary_growth_factor_monthly = (1 + salary_growth_rate)**(1./12.)
        monthly_salary = salary / 12.
        ts.loc[:, 'salary'] = (np.ones(len(index)) * salary_growth_factor_monthly).cumprod() * monthly_salary
        ts.loc[:, 'gross_savings'] = ts.loc[:, 'salary'] * savings_rate

        # Discount factor
        discount_factor_monthly = (1 + discount_rate) ** (1. / 12.)
        ts.loc[:, 'discount_factor'] = 1. / (np.ones(len(index)) * discount_factor_monthly).cumprod()
        self.ts = ts

    @staticmethod
    def _ts_to_dict(ts):
        from numpy import isnan
        return {
            k: [
                v if isinstance(v, str) or (v is not None and not isnan(v)) else None
                for v in values
            ]
            for k, values in ts.to_dict(orient='series').items()
        }
        # return [
        #     {k: v for k, v in t.items() if isinstance(v, str) or (v is not None and not isnan(v))} for t in
        #         ts.to_dict(orient='series')
        # ]

    def to_dict(self):
        return {
            'person': self.person.to_dict(),
            'scenario_name': self.scenario_name,
            'periods': self.periods,
            'start_date': self.start_date,
            'discount_rate': self.discount_rate,
            'ts': self._ts_to_dict(self.ts)
        }

    def run(self, credit_cards, status=True):
        """

        Args:
            credit_cards:
            status:

        Returns:

        """
        np.seterr(all='raise')
        name = self.scenario_name
        ts = self.ts

        scenario_ccs = [c.copy() for c in credit_cards]
        initial_balance = np.array([c.balances.sum() for c in credit_cards]).sum()

        if status:
            ittr = tqdm.tqdm(ts.iterrows(), total=len(ts))
            ittr.set_description(name)
        else:
            ittr = ts.iterrows()

        for dt, row in ittr:
            cur_date = dt.to_timestamp()
            cur_balance = np.array([c.balances.sum() for c in scenario_ccs]).sum()
            if cur_balance > 0:
                avg_apr = np.array([(c.aprs * c.balances).sum() for c in credit_cards]).sum() / cur_balance
            else:
                break  # No more simulations to do
            interest_expense = np.array([c.calc_interest_charge(date=cur_date).sum() for c in scenario_ccs]).sum()

            ts.loc[dt, 'total_cc_balance'] = cur_balance
            ts.loc[dt, 'interest_expense'] = interest_expense
            ts.loc[dt, 'avg_apr'] = avg_apr

            min_payments = np.array([c.calc_min_payments().sum() for c in scenario_ccs])
            balances = np.array([c.balances.sum() for c in scenario_ccs])
            savings = ts.loc[dt, 'gross_savings']

            if name == 'min_payment_only':
                payments = min_payments
            elif name == 'highest_rate_first':
                """Paydown the highest rate first after paying the minimums"""
                additional_paydown = max(savings - min_payments.sum(), 0)

                avg_aprs = np.array(
                    [(c.aprs * c.balances).sum() / c.balances.sum() if bal > 0 else 0 for bal, c in
                     zip(balances, scenario_ccs)]
                )
                payments = min_payments.copy()
                while additional_paydown > 0 and avg_aprs.max() >= 0:
                    idx = avg_aprs.argmax()
                    pmt = max(0, min(additional_paydown, balances[idx] - min_payments[idx]))
                    payments[idx] += pmt
                    additional_paydown -= pmt
                    avg_aprs[idx] = -1
            elif name == 'largest_balance_first':
                """Paydown the highest balance first after paying the minimums"""
                additional_paydown = max(savings - min_payments.sum(), 0)
                payments = min_payments.copy()
                ctr = 0
                while additional_paydown > 0 and ctr < len(balances):
                    idx = balances.argmax()
                    pmt = max(0, min(additional_paydown, balances[idx] - min_payments[idx]))
                    payments[idx] += pmt
                    additional_paydown -= pmt
                    ctr += 1
            elif name == 'smallest_balance_first':
                """Paydown the highest balance first after paying the minimums"""
                additional_paydown = max(savings - min_payments.sum(), 0)
                payments = min_payments.copy()
                ctr = 0
                while additional_paydown > 0 and ctr < len(balances):
                    idx = balances.argmin()
                    pmt = max(0, min(additional_paydown, balances[idx] - min_payments[idx]))
                    payments[idx] += pmt
                    additional_paydown -= pmt
                    ctr += 1
            elif name == 'optimized':
                """Paydown minimize the growth rates of all accounts"""
                avg_aprs = np.array(
                    [(c.aprs * c.balances).sum() / c.balances.sum() if bal > 0 else 0. for bal, c in
                     zip(balances, scenario_ccs)]
                    , dtype=np.float
                )
                optimal_paydown = balances * avg_aprs
                if optimal_paydown.sum() > 0:
                    optimal_paydown = optimal_paydown / optimal_paydown.sum() * savings
                elif balances.sum() > 0:
                    optimal_paydown = balances / balances.sum() * savings
                else:
                    optimal_paydown = balances * 0.0

                payments = np.clip(optimal_paydown, min_payments, balances)

                extra = max(payments.sum() - savings, 0)
                if extra > 0:
                    tmp = np.clip(optimal_paydown - min_payments, 0, optimal_paydown)
                    if tmp.sum() > 0:
                        payments -= np.clip(tmp / tmp.sum() * extra, 0, tmp)
            else:
                raise NotImplementedError("name not implemented: {}".format(name))

            # Pay at least 1 dollar to each unless the balance is < $1
            payments = np.clip(
                np.round(payments, 2),
                np.clip(np.ones(len(balances)), 0.0, balances),
                balances
            )

            shortfall = max(0, payments.sum() - savings)
            ctr = 0
            while shortfall > 0.01 and ctr < len(balances):
                # Dont pay down lowest balance
                idx = (balances - payments).argmin()
                payments[idx] -= shortfall
                payments = np.clip(payments, 0, payments)
                shortfall = max(0, payments.sum() - savings)
                ctr += 1

            if payments.sum() > savings:
                assert NotImplementedError("Couldn't make payment of {} given {} on {}".format(
                    payments.sum(), savings, dt
                ))

            ts.loc[dt, 'missed_payments'] = ((payments < min_payments)*1).sum()
            ts.loc[dt, 'late_fees'] = 0

            cc_payment = 0
            for pmt, cc, min_pmt in zip(payments, scenario_ccs, min_payments):
                cc_payment += pmt
                cc_payment -= cc.paydown(pmt)

                if min_pmt > pmt:
                    ts.loc[dt, 'late_fees'] += cc.charge_late_fee()

            ts.loc[dt, 'cc_payment'] = cc_payment

        # Calculate meta statistics
        payments_sum = ts.cc_payment.sum()
        payments_sum_pv = (ts.discount_factor * ts.cc_payment).sum()

        months_to_paydown = (ts['total_cc_balance'] > 0).sum()
        months_to_paydown_85pct = (ts['total_cc_balance'] > initial_balance * 0.15).sum()
        months_to_paydown_95pct = (ts['total_cc_balance'] > initial_balance * 0.05).sum()
        months_to_paydown_99pct = (ts['total_cc_balance'] > initial_balance * 0.01).sum()

        return {
            'name': name,
            'values': {
                'initial_balance': initial_balance,
                'payments_sum': payments_sum,
                'payments_sum_pv': payments_sum_pv,
                'months_to_paydown': months_to_paydown,
                'months_to_paydown_85pct': months_to_paydown_85pct,
                'months_to_paydown_95pct': months_to_paydown_95pct,
                'months_to_paydown_99pct': months_to_paydown_99pct,
                'late_fees': ts.late_fees.sum(),
                'missed_payments': ts.missed_payments.sum()
            },
            'ts': self._ts_to_dict(self.ts)
        }
