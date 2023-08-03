#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from datetime import datetime

from ...utils.logger import logger as log


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
    log.info("Calling calc_maximum_drawdown_duration")

    if ts is not None:
        assert len(ts) == len(
            data
        ), "The same number of data values as timestamp values are expected"

    maximum_drawdown_duration_start_index = None
    maximum_drawdown_duration_end_index = None
    mdd_duration = 0
    for i, datum in enumerate(data):
        log.debug(f"Index: {i} has value: {datum}")
        if i + 1 < len(data) - mdd_duration:
            proceeding = data[i + 1 :]  # all data after the current point
            for j, p in enumerate(proceeding, start=1):
                log.debug(f"Inner index: {j} has value: {p}")
                if p < datum and mdd_duration < j:
                    log.debug(f"Inner: {p} is less than outer: {datum}")
                    mdd_duration = j
                    maximum_drawdown_duration_start_index = i
                    maximum_drawdown_duration_end_index = i + j
                else:
                    break

    log.debug(f"MDD Duration start index: {maximum_drawdown_duration_start_index}")
    log.debug(f"MDD Duration end index: {maximum_drawdown_duration_end_index}")
    log.debug(f"MDD Duration: {mdd_duration}")

    return {
        "maximum_drawdown_duration_start_index": maximum_drawdown_duration_start_index,
        "maximum_drawdown_duration_end_index": maximum_drawdown_duration_end_index,
        "maximum_drawdown_duration_start_timestamp": ts[
            maximum_drawdown_duration_start_index
        ]
        if ts is not None and maximum_drawdown_duration_start_index is not None
        else None,
        "maximum_drawdown_duration_end_timestamp": ts[
            maximum_drawdown_duration_end_index
        ]
        if ts is not None and maximum_drawdown_duration_end_index is not None
        else None,
    }
