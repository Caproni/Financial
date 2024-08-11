#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import pandas as pd
import numpy as np

from src.utils import log


def calc_relative_strength_index(
    data: list[float | int],
    window: int = 14,
) -> list[float]:
    """
    Calculate the Relative Strength Index (RSI) for a given time series.

    Parameters:
    data (list[float | int]): A list containing the price data.
    window (int): The window size for calculating RSI, typically 14.

    Returns:
    list[float]: The RSI values for the given data.
    """
    log.function_call()

    delta = data.diff()

    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=window, min_periods=1).mean()
    avg_loss = pd.Series(loss).rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return pd.Series(rsi, index=data.index).to_list()
