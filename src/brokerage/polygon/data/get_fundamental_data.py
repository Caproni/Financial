#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from polygon import RESTClient
from datetime import datetime, timedelta

from src.brokerage.polygon.utils import get_delta
from src.utils import log


def get_fundamental_data(
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
    log.info("Calling get_fundamental_data")

    delta = get_delta(timespan)

    responses = []
    start_datetime = from_
    while start_datetime <= to:
        try:
            response = client.get_related_companies(
                ticker=ticker,
                multiplier=multiplier,
                timespan=timespan,
                from_=start_datetime,
                to=min(
                    start_datetime + delta - timedelta(seconds=1), to
                ),  # subtract a second to prevent double-counting,
                adjusted=True,
                raw=False,
                limit=50_000,
            )
            responses += response
            start_datetime += delta
        except Exception as e:
            log.error(f"Error: {e}")
            raise e
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
        for e in responses
    ]
