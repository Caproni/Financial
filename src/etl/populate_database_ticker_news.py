#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from pymongo.results import InsertManyResult
from datetime import datetime

from src.brokerage.polygon import (
    create_client,
    list_ticker_news,
)
from src.mongo import insert_data, get_data, create_mongo_client
from src.utils import log


def populate_database_ticker_news(
    published_utc_gte: datetime,
    published_utc_lt: datetime,
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

    results: list[InsertManyResult] = []
    for i, ticker in enumerate(tickers):
        log.info(f"Processing ticker: {i + 1} of {N}")
        log.info(f"Processing: {ticker}")
        
        news = list_ticker_news(
            client=polygon_client,
            ticker=ticker,
            published_utc_gte=published_utc_gte,
            published_utc_lt=published_utc_lt,
        )

        result = insert_data(
            mongo_client,
            database="financial",
            collection="ticker_news",
            documents=news,
            stop_on_key_violation=False,
        )

        results.append(result)

    return results
