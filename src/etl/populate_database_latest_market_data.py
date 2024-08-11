#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from asyncio import run
from datetime import datetime, timedelta

from src.brokerage.polygon import (
    get_market_data,
    create_polygon_client,
)
from src.sql import (
    insert_data,
    create_sql_client,
    unpack_simple_table,
)
from src.utils import log


def populate_database_latest_market_data(
    timespan: str,
    collection: Any,
    ticker: str,
    from_: datetime,
) -> bool:
    """
    Populates the database with the latest market data for a specific ticker.

    Args:
        timespan: A string specifying the timespan for market data retrieval.
        collection: Any type representing the database collection to populate.
        ticker: A string representing the specific ticker symbol.
        from_: A datetime object representing the start date for data retrieval.

    Returns:
        A boolean value indicating the success of data population for the given ticker.
    """
    log.function_call()

    polygon_client = create_polygon_client()
    database_client = create_sql_client()

    now = datetime.now()
    if "C:" in ticker or "I:" in ticker or "X:" in ticker:
        log.info("Ticker is a currency conversion (C:) or index (I:) or mutual (X:)")
        return False
    log.info(f"Processing: {ticker}")

    result = None
    if historical_bars := run(
        get_market_data(
            client=polygon_client,
            ticker=ticker,
            from_=from_,
            to=now - timedelta(days=1),
            timespan=timespan,
        )
    ):
        log.info(f"Data obtained for symbol: {ticker}")
        log.info(f"Number of documents obtained: {len(historical_bars)}")
        documents = unpack_simple_table(
            collection=collection,
            data=historical_bars,
        )
        result = insert_data(
            database_client,
            documents,
        )
        log.info(f"Data inserted for symbol: {ticker}")

    return result
