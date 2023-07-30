#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""


def get_drawdowns(
    data: list[float | int],
    as_percentage: bool = True,
) -> list[float | int]:
    """Gets a list of all drawdown values of a univariate timeseries.

    Args:
        data (list[float | int]): The timeseries data for which to calculate the maximum drawdown value.

    Returns:
        dict[str, Any]: Dictionary describing the max drawdown value.
    """

    drawdowns = []
    previous_datum = -1  # data values are assumed to be positive semi-definite
    for i, datum in enumerate(data):
        if i + 1 < len(data) and datum >= previous_datum:
            drawdown = 0
            proceeding = data[i + 1 :]  # all data after the current point
            for p in proceeding:
                if p < datum and (datum - p) > drawdown:
                    drawdown = datum - p
                else:
                    break
            if as_percentage:
                drawdown = drawdown / datum * 100
            drawdowns.append(drawdown)
            previous_datum = datum

    return drawdowns
