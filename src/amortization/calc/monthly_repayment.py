#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from src.amortization.money.money import Money


class MonthlyRepayment:
    def __init__(
        self,
        principal_loan_amount: Money,
        number_of_repayment_periods: int,
        aer_percentage: float,
        repayment_frequency: str,
    ) -> None:
        """Calculates repayments on an amortized loan such as a mortgage

        :param principal_loan_amount: The total value of the amortized loan
        :param number_of_repayment_periods: The number of payments that will be made over the lifetime of the loan
        :param aer_percentage: Annual equivalent rate as a percentage (provided by lender)
        :param repayment_frequency: Frequency of loan repayments
        """
        self.principal_loan_amount = principal_loan_amount
        self.number_of_repayment_periods = number_of_repayment_periods
        self.aer_percentage = aer_percentage
        self.repayment_frequency = repayment_frequency

        assert self.repayment_frequency in [
            "annual",
            "monthly",
            "daily",
        ], "Repayment frequency is not implemented"

    @property
    def rate(self) -> float:
        if self.repayment_frequency == "monthly":
            return self.aer_percentage / 12 / 100
        if self.repayment_frequency == "annual":
            return self.aer_percentage / 100
        raise NotImplementedError("Repayment frequency is not implemented")

    def calc_monthly_payment(
        self,
    ) -> dict[str, Money]:
        monthly_payment = (
            self.principal_loan_amount
            * (self.rate * (1 + self.rate) ** self.number_of_repayment_periods)
            / (((1 + self.rate) ** self.number_of_repayment_periods) - 1)
        )

        interest_payment = self.calc_interest_payment()
        return {
            "loan_payment": monthly_payment - interest_payment,
            "interest_payment": interest_payment,
            "total_payment": monthly_payment,
        }

    def calc_interest_payment(self) -> Money:
        return self.principal_loan_amount * self.rate
