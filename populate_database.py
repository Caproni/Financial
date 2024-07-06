#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from datetime import datetime, timedelta

from src.brokerage.polygon import (
    get_market_data,
    list_tickers,
    create_client,
    get_exchanges,
)
from src.mongo import insert_data, create_mongo_client
from src.utils import log


if __name__ == "__main__":
    log.info("Getting historical data.")

    polygon_client = create_client()
    mongo_client = create_mongo_client()

    exchanges = get_exchanges(polygon_client)
    
    result = insert_data(
        mongo_client,
        database="financial",
        collection="exchanges",
        documents=exchanges,
    )

    tickers = list_tickers(  # gets all symbols not just current ones
        polygon_client,
        market="stocks",
        active=False,
        as_list=False,
    )

    all_symbols: list[str] = []
    while True:

        try:
            s = next(tickers)
            all_symbols.append(s)
        except StopIteration as e:
            log.info("Reached end of generated tickers.")
            break

    now = datetime.now()

    for s in all_symbols:

        log.info(f"Processing: {s.ticker}")
        historical_stock_bars = get_market_data(
            polygon_client,
            ticker=s.ticker,
            timespan="day",
            from_=now - timedelta(days=12 * 365),
            to=now - timedelta(days=1),
        )

        N = len(historical_stock_bars)
        if N:
            log.info(f"Data obtained for symbol: {s.ticker}")
            log.info(f"Number of documents: {N}")
            insert_data(
                client=mongo_client,
                database="financial",
                collection="polygon_daily_historical_market_data",
                documents=historical_stock_bars,
            )
    log.info("Finished getting historical data.")
