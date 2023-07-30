#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""


def calc_maximum_drawdown_value(
    data: list[float | int],
) -> dict[str, float | int | None]:
    """Calculates the maximum drawdown value of a univariate timeseries.

    Args:
        data (list[float | int]): The timeseries data for which to calculate the maximum drawdown value.

    Returns:
        dict[str, Any]: Dictionary describing the max drawdown value.
    """

    maximum_drawdown_max_index = None
    maximum_drawdown_min_index = None
    maximum_drawdown_percentage = 0
    maximum_drawdown_value = None
    for i, datum in enumerate(data):
        if i + 1 < len(data):
            proceeding = data[i + 1 :]  # all data after the current point
            for j, p in enumerate(proceeding, start=1):
                if (
                    p < datum
                    and maximum_drawdown_percentage < (datum - p) / datum * 100
                ):
                    maximum_drawdown_percentage = (datum - p) / datum * 100
                    maximum_drawdown_value = datum - p
                    maximum_drawdown_max_index = i
                    maximum_drawdown_min_index = i + j

    return {
        "maximum_drawdown_max_index": maximum_drawdown_max_index,
        "maximum_drawdown_min_index": maximum_drawdown_min_index,
        "maximum_drawdown_value": maximum_drawdown_value,
        "maximum_drawdown_value_percentage": maximum_drawdown_value
        / data[maximum_drawdown_max_index]
        * 100
        if maximum_drawdown_value is not None
        else None,
    }
