#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from datetime import datetime

from .calc_average_annualized_return import calc_average_annualized_return
from .calc_maximum_drawdown_value import calc_maximum_drawdown_value


def calc_calmar_ratio(
    data: list[float | int],
    ts: list[datetime],
) -> float:
    """Calculates the Calmar ratio for timeseries data, which is the ratio between the AAR (numerator) and the max drawdown (denominator)

    Args:
        data (list[float | int]): The timeseries data for which to calculate the Calmar ratio.

    Returns:
        float: The Calmar ratio
    """

    assert len(data) == len(
        ts
    ), "The same number of data values as timestamp values are expected"

    return (
        calc_average_annualized_return(
            start_value=data[0],
            end_value=data[-1],
            start_time=ts[0],
            end_time=ts[-1],
        )
        / calc_maximum_drawdown_value(data)["maximum_drawdown_value_percentage"]
    )
