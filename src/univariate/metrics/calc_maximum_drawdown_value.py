#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

def calc_maximum_drawdown_value(
    data: list[float | int],
) -> dict[str, float | int | None]:
    """Calculates the maximum drawdown value of a univariate timeseries.
        The maximum drawdown value is the maximum decrease since the high water mark of the timeseries.

    Args:
        data (list[float | int]): The timeseries data for which to calculate the maximum drawdown value.

    Returns:
        dict[str, Any]: Dictionary describing the max drawdown value.
    """
    
    high_water_mark = max(data)
    high_water_mark_index = data.index(high_water_mark)
    
    return {
        "high_water_mark": high_water_mark,
        "maximum_drawdown_value":  high_water_mark - min(data[high_water_mark_index:]),
    }