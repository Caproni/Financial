#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from .get_drawdowns import get_drawdowns
from ...utils.logger import logger as log


def calc_average_drawdown(
    data: list[int | float],
) -> float:
    """Calculates the average (mean) drawdown of timeseries data

    Args:
        data (list[int | float]): Timeseries data for which to calculate the average drawdown

    Returns:
        float: The average drawdown
    """
    log.info("Calling calc_average_drawdown")

    drawdowns = get_drawdowns(data)

    return sum(drawdowns) / len(drawdowns)
