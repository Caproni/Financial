#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import pandas as pd
from statsmodels.tsa.vector_ar.vecm import coint_johansen

from ..utils.logger import logger as log


def calc_johansen_test(
    v1: list[float | int],
    v2: list[float | int],
    lag: int = 0,
) -> dict[str, str]:
    """Calculate the Johansen test statistic for two time-series.

    Args:
        v1 (list[float | int]): First time-series.
        v2 (list[float | int]): Second time-series.
        lag (int, optional): The number of lagged difference terms to include in the model. Defaults to 0.

    Returns:
        dict[str, str]: The results of the test.
    """
    log.function_call()
    
    N1 = len(v1)
    N2 = len(v2)
    
    if N1 > N2:
        log.warning("Arrays not of same length. Truncating first time-series.")
        v1 = v1[:N2]
    elif N2 > N1:
        log.warning("Arrays not of same length. Truncating second time-series.")
        v2 = v2[:N1]

    df = pd.DataFrame(
        {
            "v1": v1,
            "v2": v2,
        }
    )
    result = coint_johansen(df, det_order=0, k_ar_diff=lag)

    log.info(f"Eigenvalue Statistic: {result.lr1}")
    log.info(f"Critical Values (90%, 95%, 99%): {result.cvt}")

    p_values = [
        "99%",
        "95%",
        "90%",
    ]

    johansen_test_results = {
        0: "null hypothesis accepted",
        1: "null hypothesis accepted",
    }

    eigenvalues = [float(e) for e in result.lr1]
    for i, eigenvalue in enumerate(eigenvalues):
        critical_values = [float(e) for e in result.cvt[i]]
        critical_values.reverse()
        for p, critical_value in enumerate(critical_values):
            if eigenvalue > critical_value:
                log.info(
                    f"Eigenvalue: {eigenvalue} exceeds threshold: {critical_value} at p: {p_values[p]}"
                )
                johansen_test_results[i] = f"null hypothesis rejected at {p_values[p]}"
                break

    return johansen_test_results
