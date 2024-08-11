#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from math import exp
from statistics import mean, stdev

from ...utils.logger import logger as log


def calc_linear_moving_average(
    data: list[float | int],
    steps: int = None,
) -> tuple[list[float | int], list[float | int]]:
    log.function_call()

    if not data:
        log.warning("Input data vector is empty.")
        return data

    ma_data_mean, ma_data_sd = [], []
    for i in range(len(data)):
        lower = max(0, i - steps) if steps is not None else 0
        subset = data[lower : i + 1]
        ma_data_mean.append(mean(subset))
        ma_data_sd.append(stdev(subset) if len(subset) > 1 else None)

    return ma_data_mean, ma_data_sd
