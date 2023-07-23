from datetime import datetime
import matplotlib.pyplot as plt

from src.amortization.calc.amortized_loan import AmortizedLoan
from src.amortization.calc.monthly_repayment import MonthlyRepayment
from src.amortization.money.money import Money
from src.amortization.data.bank_of_england_baserates import load_base_rate_data

if __name__ == "__main__":
    now = datetime.now()

    data = load_base_rate_data("data/bank_of_england_historical_base_rates.csv")

    data.plot(x="Date Changed", y="Rate")
    plt.show()

    principal_loan_amount = Money(
        currency="GBP",
        when=now,
        integral=135138 - 40000,
        mantissa=0,
    )

    repayment_periods = 10 * 12 + 9

    aer_percentage = 4.79
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
