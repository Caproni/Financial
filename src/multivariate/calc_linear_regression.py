#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import pandas as pd
from scipy.stats import linregress

from src.utils import log


def calc_linear_regression(
    data_1: list[int | float],
    data_2: list[int | float],
):
    """
    Perform a linear regression between two time-series.

    Parameters:
    - data_1: pandas Series representing the first time-series (independent variable, X).
    - data_2: pandas Series representing the second time-series (dependent variable, Y).

    Returns:
    - regression_results: A dictionary containing the slope, intercept, r_value, p_value, and std_err of the regression.
    """
    log.function_call()

    if len(data_1) != len(data_2):
        raise ValueError("The two time-series must have the same length.")

    slope, intercept, r_value, p_value, std_err = linregress(
        pd.Series(data_1), pd.Series(data_2)
    )

    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "r2_value": float(r_value) ** 2,
        "p_value": float(p_value),
        "std_err": float(std_err),
    }
