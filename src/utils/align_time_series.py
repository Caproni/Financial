#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from datetime import datetime

from ..utils.logger import logger as log


def align_time_series(
    datetime1: list[datetime],
    values1: list[float | int],
    datetime2: list[datetime],
    values2: list[float | int],
) -> tuple[list[datetime], list[float | int], list[float | int]]:
    """
    Align two time-series by their datetime lists.

    Parameters:
    datetime1 (list of datetime): Datetimes corresponding to the first time-series.
    values1 (list of float): Values of the first time-series.
    datetime2 (list of datetime): Datetimes corresponding to the second time-series.
    values2 (list of float): Values of the second time-series.

    Returns:
    list of datetime, list of float, list of float: Aligned datetimes, values1, and values2.
    """
    log.function_call()

    common_datetimes = sorted(set(datetime1).intersection(set(datetime2)))

    datetime_to_value1 = dict(zip(datetime1, values1))
    datetime_to_value2 = dict(zip(datetime2, values2))

    # Align the values based on the common datetimes
    aligned_values1 = [datetime_to_value1[dt] for dt in common_datetimes]
    aligned_values2 = [datetime_to_value2[dt] for dt in common_datetimes]

    return common_datetimes, aligned_values1, aligned_values2
