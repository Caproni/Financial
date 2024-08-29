#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from asyncio import to_thread, Task, gather
from typing import Any
from polygon import RESTClient
from datetime import datetime, timedelta

from src.brokerage.polygon.utils import get_delta
from src.utils import log


async def get_market_data_async(
    polygon_client: RESTClient,
    ticker: str,
    timespan: str,
    delta: timedelta,
    multiplier: int,
    start_datetime: datetime,
    to: datetime,
    subtract_day: bool = True,
):
    offset = timedelta(days=1) if subtract_day else timedelta(days=0)
    return await to_thread(
        polygon_client.get_aggs,
        ticker=ticker,
        multiplier=multiplier,
        timespan=timespan,
        from_=start_datetime,
        to=min(start_datetime + delta - offset, to),
        adjusted=True,
        raw=False,
        limit=50_000,
    )


async def get_market_data(
    client: RESTClient,
    ticker: str,
    from_: datetime,
    to: datetime,
    timespan: str,
    multiplier: int = 1,
    subtract_day: bool = True,
) -> list[dict[str, Any]]:
    """Gets market data from Polygon.io.

    Args:
        client (RESTClient): A Polygon client.
        ticker (str): A specific ticker / symbol.
        from_ (datetime): Start date for data.
        to (datetime): End date for data.
        timespan (str): Frequency of data.
        multiplier (int, optional): Number of "timespans". Defaults to 1.
        subtract_day (bool): Whether to subtract a day to prevent the same data being retrieved twice.

    Returns:
        list[dict[str, Any]]: A list of dictionaries representing bars.
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

    delta = get_delta(timespan)

    tasks: list[Task] = []
    start_datetime = from_
    while start_datetime <= to:
        try:
            tasks.append(
                get_market_data_async(
                    polygon_client=client,
                    ticker=ticker,
                    timespan=timespan,
                    delta=delta,
                    multiplier=multiplier,
                    start_datetime=start_datetime,
                    to=to,
                    subtract_day=subtract_day,
                )
            )

            start_datetime += delta

        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    responses: list[dict[str, Any]] = []
    if tasks:
        batch_results = await gather(*tasks)
        responses = [r for result in batch_results for r in result if result]

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
