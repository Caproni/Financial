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
    create_client,
)
from src.sql import insert_data, get_data, create_sql_client, unpack_simple_table, Tickers, PolygonMarketDataDay
from src.utils import log


def populate_database_market_data(
    timespan: str,
    collection: Any,
) -> list[bool]:
    log.function_call()

    polygon_client = create_client()
    database_client = create_sql_client()

    tickers = get_data(
        database_client,
        models=[Tickers],
    )

    N = len(tickers)

    now = datetime.now()
    results: list[bool] = []
    for i, s in enumerate(tickers):
        if "C:" in s["ticker"] or "I:" in s["ticker"] or "X:" in s["ticker"]:
            log.info(
                "Ticker is a currency conversion (C:) or index (I:) or mutual (X:)"
            )
            continue
        log.info(f"Processing ticker {i + 1} of {N}")
        log.info(f"Processing: {s['ticker']}")

        result = None
        if historical_bars := run(
            get_market_data(
                polygon_client,
                s["ticker"],
                now - timedelta(days=365 * 5 + 1),
                now - timedelta(days=1),
                timespan,
            )
        ):
            log.info(f"Data obtained for symbol: {s['ticker']}")
            log.info(f"Number of documents obtained: {len(historical_bars)}")
            documents = unpack_simple_table(
                collection=collection,
                data=historical_bars,
            )
            result = insert_data(
                database_client,
                documents,
            )
            log.info(f"Data inserted for symbol: {s['ticker']}")

        results.append(result)

    return results
