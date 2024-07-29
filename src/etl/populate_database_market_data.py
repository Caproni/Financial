#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from asyncio import run
from pymongo.results import InsertManyResult
from datetime import datetime, timedelta

from src.brokerage.polygon import (
    get_market_data,
    create_client,
)
from src.mongo import insert_data, get_data, create_mongo_client
from src.utils import log


def populate_database_market_data(
    timespan: str,
    collection: str,
) -> list[InsertManyResult]:
    log.info("Calling populate_database_market_data")

    polygon_client = create_client()
    mongo_client = create_mongo_client()

    tickers = get_data(
        mongo_client,
        database="financial",
        collection="tickers",
        pipeline=None,
    )

    N = len(tickers)

    now = datetime.now()
    results: list[InsertManyResult] = []
    for i, s in enumerate(tickers):
        if "C:" in s["ticker"] or "I:" in s["ticker"] or "X:" in s["ticker"]:
            log.info(
                "Ticker is a currency conversion (C:) or index (I:) or mutual (X:)"
            )
            continue
        log.info(f"Processing ticker {i + 1} of {N}")
        log.info(f"Processing: {s['ticker']}")
                
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
            result = insert_data(
                mongo_client,
                "financial",
                collection,
                historical_bars,
            )
            log.info(f"Data inserted for symbol: {s['ticker']}")
        
        results.append(result)

    return results
