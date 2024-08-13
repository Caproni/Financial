#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
import pandas as pd
from statsmodels.tsa.stattools import coint

from src.utils import log


def calc_cadf(
    data_1: list[int | float],
    data_2: list[int | float],
) -> dict[str, Any]:
    """
    Calculate the Cointegrated Augmented Dickey-Fuller (CADF) test parameter for two time-series.

    Parameters:
    - data_1: List or array-like object representing the first time-series.
    - data_2: List or array-like object representing the second time-series.

    Returns:
    - cadf_results: A dictionary containing the CADF statistic, p-value, and critical values.
    """
    log.function_call()

    N1 = len(data_1)
    N2 = len(data_2)

    if N1 > N2:
        log.warning("Arrays not of same length. Truncating first time-series.")
        data_1 = data_1[:N2]
    elif N2 > N1:
        log.warning("Arrays not of same length. Truncating second time-series.")
        data_2 = data_2[:N1]

    coint_result = coint(
        pd.Series(data_1),
        pd.Series(data_2),
    )

    return {
        "CADF Statistic": float(coint_result[0]),
        "p-value": float(coint_result[1]),
        "Critical Values": [float(e) for e in coint_result[2]],
    }
