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
    log.info("Calling calc_johansen_test")

    df = pd.DataFrame(
        {
            "v1": v1,
            "v2": v2,
        }
    )
    return coint_johansen(df, det_order=0, k_ar_diff=lag)
