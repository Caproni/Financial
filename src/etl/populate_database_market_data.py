#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import asyncio
from polygon import RESTClient
from pymongo import MongoClient
from pymongo.results import InsertManyResult
from datetime import datetime, timedelta

from src.brokerage.polygon import (
    get_market_data,
    create_client,
)
from src.mongo import insert_data, get_data, create_mongo_client
from src.utils import log


async def process_ticker(
    mongo_client: MongoClient, 
    polygon_client: RESTClient, 
    ticker: str, 
    timespan: str, 
    from_: datetime, 
    to: datetime, 
    collection: str,
    semaphore: asyncio.Semaphore,
) -> InsertManyResult | None:
    log.info("Calling process_ticker")
    async with semaphore:
        historical_bars = await asyncio.to_thread(
            get_market_data,
            polygon_client,
            ticker,
            from_,
            to,
            timespan,
        )

    if historical_bars:
        log.info(f"Data obtained for symbol: {ticker}")
        log.info(f"Number of documents obtained: {len(historical_bars)}")
        result = await asyncio.to_thread(
            insert_data,
            mongo_client,
            "financial",
            collection,
            historical_bars,
        )
        log.info(f"Data inserted for symbol: {ticker}")
        return result
    return None


async def populate_database_market_data(
    timespan: str,
    collection: str,
    batch_size: int = 10,
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
    tasks: list[asyncio.Task] = []
    for i, s in enumerate(tickers):
        if "C:" in s["ticker"] or "I:" in s["ticker"] or "X:" in s["ticker"]:
            log.info("Ticker is a currency conversion (C:) or index (I:) or mutual (X:)")
            continue
        log.info(f"Processing ticker {i + 1} of {N}")
        log.info(f"Processing: {s['ticker']}")
        tasks.append(
            process_ticker(
                mongo_client,
                polygon_client,
                s["ticker"],
                timespan,
                now - timedelta(days=365 * 5 + 1),
                now - timedelta(days=1),
                collection=collection,
                semaphore=asyncio.Semaphore(batch_size),
            )
        )
        
        if len(tasks) >= batch_size:
            batch_results = await asyncio.gather(*tasks)
            results.extend([result for result in batch_results if result])
            tasks = []

    if tasks:  # final set of results
        batch_results = await asyncio.gather(*tasks)
        results.extend([result for result in batch_results if result])

    return results
