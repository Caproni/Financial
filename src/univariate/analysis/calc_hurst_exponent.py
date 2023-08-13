#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from statistics import stdev

from ...utils.logger import logger as log


def calc_hurst_exponent(
    data: list[int | float],
) -> float:
    """Calculates the Hurst exponent as per: https://en.m.wikipedia.org/wiki/Hurst_exponent

    Args:
        data (list[int | float]): Timeseries data for which to calculate the Hurst exponent

    Returns:
        float: The Hurst Exponent
    """
    log.info("Calling calc_hurst_exponent")

    N = len(data)

    assert N > 8, "Insufficient data has been provided"

    data_av = sum(data) / N
    normed_data = [d - data_av for d in data]
    zs = [sum(normed_data[: i + 1]) for i in range(N)]
    r = [max(zs[: i + 1]) - min(zs[: i + 1]) for i in range(N)]
    st_devs = [stdev(data[:i + 1]) for i in range(N)]
    return [r[i] / st_devs[i] for i in range(N)]  # TODO: fix!
