#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.enums import Adjustment, DataFeed
from datetime import datetime

from src.utils.logger import logger as log


def get_stock_bars(
    client: StockHistoricalDataClient,
    symbols: list[str],
    start: datetime = None,
    end: datetime = None,
):
    log.info("Calling get_stock_bars")
    client.get_stock_bars(
        StockBarsRequest(
            symbol_or_symbols=symbols,
            start=start,
            end=end,
            adjustment=Adjustment.ALL,
        )
    )
