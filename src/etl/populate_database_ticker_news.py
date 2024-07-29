#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from asyncio import Task, to_thread, gather
from polygon import RESTClient
from pymongo.results import InsertManyResult
from datetime import datetime, timedelta

from src.brokerage.polygon import (
    create_client,
    list_ticker_news,
)
from src.mongo import insert_data, get_data, create_mongo_client
from src.utils import log


async def process_ticker(
    polygon_client: RESTClient,
    ticker: str,
    published_utc_gte: datetime,
    published_utc_lt: datetime,
) -> list[dict[str, Any]]:
    log.info("Calling process_ticker")
    return await to_thread(
        list_ticker_news,
        polygon_client,
        ticker,
        published_utc_gte,
        published_utc_lt,
    )


async def populate_database_ticker_news(
    start_time: datetime,
    finish_time: datetime,
    tickers: list[str] | None = None,
) -> list[InsertManyResult]:
    """Populate database with news articles related to specific tickers.

    Args:
        published_utc_gte (datetime): Lower bound on article publication date (gte = greater than or equal).
        published_utc_lt (datetime): Upper bound on article publication date (lt = less than).
        tickers (list[str], optional): A list of tickers to process. Defaults to None in which case all tickers are obtained from database and processed.

    Returns:
        list[InsertManyResult]: A list of insertion results for news data.
    """
    log.info("Calling populate_database_ticker_news")

    polygon_client = create_client()
    mongo_client = create_mongo_client()

    offset_days = 300  # number of days in each asynchronous data request

    if tickers is None:
        tickers = get_data(
            mongo_client,
            database="financial",
            collection="tickers",
            pipeline=None,
        )
        tickers = [ticker["ticker"] for ticker in tickers]

    N = len(tickers)

    log.info(f"Processing: {N} tickers.")

    insert_results: list[InsertManyResult] = []
    for i, ticker in enumerate(tickers):
        log.info(f"Processing ticker: {i + 1} of {N}")
        log.info(f"Processing: {ticker}")

        tasks: list[Task] = []
        all_news: list[dict[str, Any]] = []

        published_utc_lt = finish_time
        published_utc_gte = published_utc_lt - timedelta(days=offset_days)

        while start_time < published_utc_lt:
            tasks.append(
                process_ticker(
                    polygon_client,
                    ticker,
                    published_utc_gte,
                    published_utc_lt,
                )
            )
            published_utc_lt = published_utc_gte
            published_utc_gte -= timedelta(days=offset_days)

        batch_results = await gather(*tasks)
        if all_news := [b for batch in batch_results for b in batch if batch]:
            result = insert_data(
                mongo_client,
                database="financial",
                collection="ticker_news",
                documents=all_news,
                stop_on_key_violation=False,
            )

            insert_results.append(result)

    return insert_results
