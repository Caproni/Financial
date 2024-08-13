#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import statsmodels.api as sm
import numpy as np

from src.utils import log


def calc_linear_regression(
    data_1: list[int | float],
    data_2: list[int | float],
    add_intercept: bool = False,
):
    """
    Calculates the linear regression between two sets of data.

    Args:
        data_1: A list of integers or floats representing the first set of data.
        data_2: A list of integers or floats representing the second set of data.
        add_intercept: A boolean indicating whether to include an intercept in the regression (default is False).

    Returns:
        A dictionary containing the slope, intercept, R-squared value, p-value, and standard error of the regression.
    Raises:
        ValueError: If the lengths of the two data sets are not equal.
    """
    log.function_call()

    if len(data_1) != len(data_2):
        raise ValueError("The two time-series must have the same length.")

    x = np.array(data_1)
    y = np.array(data_2)

    if add_intercept:
        x = sm.add_constant(x)

    model = sm.OLS(y, x).fit()

    results = {
        "slope": float(model.params[0]),
        "r2_value": float(model.rsquared),
        "p_value": float(model.pvalues),
        "std_err": float(model.bse),
    }

    if add_intercept:
        results["slope"] = float(model.params[1])
        results["intercept"] = float(model.params[0])

    return results
