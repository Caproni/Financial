#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from datetime import timedelta

from src.utils import log


def get_delta(timespan: str) -> timedelta:
    """Get timedelta for market data queries. This timedelta should be used to chunk requests for data.

    Args:
        timespan (str): A timespan defined on the polygon.io website.

    Returns:
        timedelta: A timedelta to use when querying data. i.e. from_=start_datetime, to=start_datetime + delta
    """
    log.function_call()

    assert timespan in {
        "second",
        "minute",
        "hour",
        "day",
        "week",
        "month",
        "quarter",
        "year",
    }, "Selected timespan is not supported."

    match timespan:
        case "second":  # 12-hour windows (base aggregation type is assumed second)
            delta = timedelta(seconds=60 * 60 * 12)
        case "minute":  # one-month windows (base aggregation type is minute)
            delta = timedelta(days=30)
        case "hour":  # one-month windows (base aggregation type is minute)
            delta = timedelta(days=30)
        case (
            "day" | "week" | "month" | "quarter" | "year"
        ):  # five-year windows (base aggregation type is day)
            delta = timedelta(days=365 * 5)

    return delta
