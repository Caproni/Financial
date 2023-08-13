#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from datetime import datetime
from alpaca.trading.client import TradingClient
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

from src.brokerage.alpaca.trading.get_assets import get_assets
from src.brokerage.alpaca.data.get_stock_bars import get_stock_bars
from src.utils.logger import logger as log


def get_historical_data(
    trading_client: TradingClient,
    historical_stock_client: StockHistoricalDataClient,
    start: datetime | None = None,
    end: datetime | None = None,
):
    log.info("Calling get_historical_data")

    historical_assets = get_assets(
        trading_client,
        asset_class="us_equity",
    )

    return get_stock_bars(
        historical_stock_client,
        symbols=sorted([s.symbol for s in historical_assets]),
        timeframe=TimeFrame(
            amount=15,
            unit=TimeFrameUnit.Minute,
        ),
        start=start,
        end=end,
    )
