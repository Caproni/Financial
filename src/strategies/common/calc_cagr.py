#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from src.utils import log


def calculate_cagr(
    initial_value: float,
    final_value: float,
    periods: int,
) -> float:
    """
    Calculate the Compound Annual Growth Rate (CAGR).

    :param initial_value: The initial value of the investment.
    :param final_value: The final value of the investment.
    :param periods: The number of periods (years) over which the investment grows.
    :return: The CAGR as a decimal.
    """
    log.function_call()

    if initial_value <= 0 or final_value <= 0 or periods <= 0:
        raise ValueError(
            "Initial value, final value, and periods must be greater than zero."
        )

    return (final_value / initial_value) ** (1 / periods) - 1
