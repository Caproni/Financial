#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from datetime import datetime, timedelta

from ...utils.logger import logger as log


def calc_average_annualized_return(
    start_value: float | int,
    end_value: float | int,
    start_time: datetime,
    end_time: datetime,
) -> float:
    """Calculates the average annualized return for the timeseries data

    Args:
        data (list[float | int]): The timeseries data for which to calculate the maximum drawdown value.

    Returns:
        float: The averaged annualized return for the timeseries data
    """
    log.function_call()

    exact_year = timedelta(days=365, hours=24 / 4)
    return (end_value - start_value) * exact_year / (end_time - start_time) * 100
