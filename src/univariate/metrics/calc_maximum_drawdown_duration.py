#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from typing import Any
from datetime import datetime


def calc_maximum_drawdown_duration(
    data: list[float | int],
    ts: list[datetime] = None,
) -> dict[str, float | int | datetime | None]:
    """Calculates the maximum drawdown duration of a univariate timeseries.
        The maximum drawdown value is the maximum decrease since the high water mark of the timeseries.

    Args:
        data (list[float | int]): The timeseries data for which to calculate the maximum drawdown value.
        ts (list[datetime]): An optional list of timestamps for each value in the univariate series. Defaults to None.

    Returns:
        dict[str, Any]: Dictionary describing the max drawdown duration.
    """
    
    high_water_mark = max(data)
    high_water_mark_index = data.index(high_water_mark)
    
    if ts is not None:
        assert len(ts) == len(data), "The same number of data values as timestamp values are expected"
    
    return {
        "high_water_mark": high_water_mark,
        "high_water_mark_index": high_water_mark_index,
        "maximum_drawdown_duration":  high_water_mark - min(data[high_water_mark_index:]),
    }