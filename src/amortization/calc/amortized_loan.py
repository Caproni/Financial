#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from typing import Union
from datetime import datetime

from src.amortization.money.money import Money
from src.amortization.calc.monthly_repayment import MonthlyRepayment


class AmortizedLoan:
    def __init__(
        self,
        principal_loan_amount: Money,
        number_of_repayment_periods: int,
        aer_percentage: Union[float, list[dict[str, Union[datetime, float]]]],
        repayment_frequency: str,
        start_date: datetime,
    ):
        """A calculator to determine the total amount paid towards a loan, including interest payments

        :param principal_loan_amount: The total value of the amortized loan
        :param number_of_repayment_periods: The number of payments that will be made over the lifetime of the loan
        :param aer_percentage: Either a single float representing a annual equivalent rate percentage or a
        list of interest rates and the times that these rates came into effect
        :param repayment_frequency: Frequency of loan repayments
        :param start_date: The date that the loan came into effect
        """
        self.principal_loan_amount = principal_loan_amount
        self.number_of_repayment_periods = number_of_repayment_periods
        self.aer_percentage = aer_percentage
        self.repayment_frequency = repayment_frequency
        self.start_date = start_date

    def calc_monthly_repayments(self):
        principal_loan_amount = self.principal_loan_amount
        number_of_repayment_periods = self.number_of_repayment_periods
        total_interest_payment = Money(
            currency=self.principal_loan_amount.currency,
            when=self.principal_loan_amount.when,
            integral=0,
            mantissa=0,
        )
        while number_of_repayment_periods > 0:
            mr = MonthlyRepayment(
                principal_loan_amount=principal_loan_amount,
                number_of_repayment_periods=number_of_repayment_periods,
                aer_percentage=self.aer_percentage,
                repayment_frequency=self.repayment_frequency,
            )
            payment = mr.calc_monthly_payment()
            number_of_repayment_periods -= 1
            principal_loan_amount -= payment["loan_payment"]
            total_interest_payment += payment["interest_payment"]

        return total_interest_payment
