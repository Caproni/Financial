#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from math import sqrt

from .get_drawdowns import get_drawdowns
from ...utils.logger import logger as log


def calc_ulcer_index(
    data: list[int | float],
) -> float:
    """Calculates the Ulcer Index for a timeseries

    Args:
        data (list[int | float]): Timeseries data for which to calculate the Ulcer index

    Returns:
        float: The Ulcer index
    """
    log.info("Calling calc_ulcer_index")

    drawdowns = get_drawdowns(data)

    return sqrt(sum([d**2 for d in drawdowns]) / len(drawdowns))
