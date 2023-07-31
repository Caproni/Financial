#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from math import exp
from statistics import mean, stdev

from ...utils.logger import logger as log


def get_moving_average(
    data: list[float | int],
    weighting: str,
    steps: int = None,
) -> (list[float | int], list[float | int]):
    log.info("Calling get_moving_average")

    if not data:
        log.warning("Input data vector is empty.")
        return data

    assert weighting in {
        "linear",
        "exponential",
    }, "The moving average type is not recognized."

    if weighting != "exponential" and steps is None:
        log.error(
            "Only exponential weighting allows steps to be None. In this case all values are used"
        )
        raise ValueError(
            "Only exponential weighting allows steps to be None. In this case all values are used"
        )

    ma_data_mean, ma_data_sd = [], []
    for i in range(len(data)):
        lower = max(0, i - steps) if steps is not None else 0
        upper = min(len(data), i + steps) if steps is not None else len(data)
        if weighting == "linear":
            subset = data[lower:upper]
        elif weighting == "exponential":
            subset = [exp(-abs(i - j)) * d for j, d in enumerate(data[lower:upper])]
        ma_data_mean.append(mean(subset))
        ma_data_sd.append(stdev(subset))

    return ma_data_mean, ma_data_sd
