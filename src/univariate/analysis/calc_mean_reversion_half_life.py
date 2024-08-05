#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from statsmodels.api import add_constant, OLS
import pandas as pd
import numpy as np

from ...utils.logger import logger as log


def calc_mean_reversion_half_life(
    data: list[int | float],
) -> float:
    """Calculates the half-life of reversion to the mean for timeseries data. Shorter half-lives suggest more of a reversive character.

    Args:
        data (list[int | float]): Timeseries data for which to calculate the mean reversion half-life.

    Returns:
        float: The half-life of mean reversion, in units of the input timeseries (i.e. a result of 36 for 15-minute data would indicate a half-life of 36 * 15 minutes = 9 hours)
    """
    log.function_call()

    df = pd.DataFrame({"price": data})

    df["returns"] = df["price"].diff()
    df = df.dropna()
    df["lagged_returns"] = df["returns"].shift(1)
    df = df.dropna()

    X = add_constant(df["lagged_returns"])
    model = OLS(df["returns"], X).fit()
    theta = model.params["lagged_returns"]
    return -np.log(2) / np.log(1 + theta)
