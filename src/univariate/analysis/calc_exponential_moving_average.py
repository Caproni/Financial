#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import pandas as pd

from src.utils import log


def calc_exponential_moving_average(
    data: list[int | float],
    span: int = 3,
) -> list[float]:
    """
    Calculate the Exponential Moving Average (EMA) for a given time-series.

    Parameters:
    - data: pandas DataFrame containing the time-series data.
    - span: the span (or number of periods) to use for the EMA calculation.

    Returns:
    - list containing the EMA values.
    """

    log.function_call()

    df = pd.DataFrame({"Price": data})

    return df["Price"].ewm(span=span, adjust=False).mean().to_list()
