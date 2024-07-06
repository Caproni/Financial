#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from polygon import RESTClient
from datetime import datetime

from src.utils import log


def get_market_data(
    client: RESTClient,
    ticker: str,
    from_: datetime,
    to: datetime,
    timespan: str,
    multiplier: int = 1,
) -> list[dict[str, Any]]:
    """Gets market data from Polygon.io.

    Args:
        client (RESTClient): A Polygon client.
        ticker (str): A specific ticker / symbol.
        from_ (datetime): Start date for data.
        to (datetime): End date for data.
        timespan (str): Frequency of data.
        multiplier (int, optional): Number of "timespans". Defaults to 1.

    Returns:
        list[dict[str, Any]]: A list of dictionaries representing bars.
    """
    log.info("Calling get_market_data")

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

    try:
        response = client.get_aggs(
            ticker=ticker,
            multiplier=multiplier,
            timespan=timespan,
            from_=from_,
            to=to,
            adjusted=True,
            raw=False,
        )
    except Exception as e:
        log.error(f"Error: {e}")
        return []
    return [
        {
            "symbol": ticker,
            "open": e.open,
            "high": e.high,
            "low": e.low,
            "close": e.close,
            "otc": e.otc,
            "timestamp": datetime.fromtimestamp(e.timestamp / 1000.0),
            "transactions": e.transactions,
            "volume": e.volume,
            "vwap": e.vwap,
        }
        for e in response
    ]
