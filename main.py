from datetime import datetime

from amor.calc.amortized_loan import AmortizedLoan
from amor.calc.monthly_repayment import MonthlyRepayment
from amor.money.money import Money

if __name__ == "__main__":
    now = datetime.now()

    principal_loan_amount = Money(
        currency="GBP",
        when=now,
        integral=135519,
        mantissa=0,
    )

    repayment_periods = 18 * 12 + 10

    aer_percentage = 4.54
    repayment_frequency = "monthly"

    loan = MonthlyRepayment(
        principal_loan_amount=principal_loan_amount,
        number_of_repayment_periods=repayment_periods,
        aer_percentage=aer_percentage,
        repayment_frequency=repayment_frequency,
    )

    print(loan.calc_monthly_payment())

    loan = AmortizedLoan(
        principal_loan_amount=principal_loan_amount,
        number_of_repayment_periods=repayment_periods,
        aer_percentage=aer_percentage,
        repayment_frequency=repayment_frequency,
        start_date=datetime.fromisoformat("2018-03-25"),
    )

    total_interest_paid = loan.calc_monthly_repayments()

    print(f"{round(total_interest_paid / principal_loan_amount * 100)}%")
