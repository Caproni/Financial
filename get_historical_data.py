#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import timedelta

from src.brokerage.alpaca.broker.get_clock import get_clock
from src.brokerage.alpaca.client import create_trading_client, create_historical_stock_data_client, create_broker_client
from src.brokerage.alpaca.data import get_stock_bars
from src.brokerage.alpaca.trading.get_assets import get_assets
from src.mongo import insert_daily_bars, create_mongo_client
from src.utils import log


if __name__ == "__main__":
    log.info("Getting historical data.")

    alpaca_trading_client = create_trading_client(paper=True)
    alpaca_historical_stock_client = create_historical_stock_data_client()
    alpaca_broker_client = create_broker_client()
    mongo_client = create_mongo_client()

    alpaca_clock = get_clock(alpaca_broker_client)

    symbols = get_assets(  # gets all symbols not just current symbols
        alpaca_trading_client,
        asset_class="us_equity",
    )

    filtered_symbols = [s.symbol for s in symbols if s.symbol == "AAPL"]

    for s in filtered_symbols:
        log.info(f"Processing: {s}")
        historical_stock_bars = get_stock_bars(
            alpaca_historical_stock_client,
            symbols=[s],
            timeframe=TimeFrame(
                amount=1,
                unit=TimeFrameUnit.Day,
            ),
            start=alpaca_clock.timestamp - (timedelta(days=7)),
            end=None,
        )

        insert_daily_bars(
            client=mongo_client,
            database="financial",
            collection="daily",
            daily_bars=[dict(e) for e in historical_stock_bars[s]],
        )
    log.info("Finished getting historical data.")
