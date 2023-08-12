#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.enums import Adjustment
from alpaca.data.timeframe import TimeFrame
from alpaca.data.models import BarSet
from datetime import datetime

from src.utils.logger import logger as log


def get_stock_bars(
    client: StockHistoricalDataClient,
    symbols: list[str],
    timeframe: TimeFrame,
    start: datetime = None,
    end: datetime = None,
) -> BarSet:
    """Gets historical stock data

    Args:
        client (StockHistoricalDataClient): An Alpaca data client.
        symbols (list[str]): A list of symbols for which to obtain data.
        timeframe (TimeFrame): The frequency of data to obtain.
        start (datetime, optional): Start datetime for data retrieval. Defaults to None.
        end (datetime, optional): End datetime for data retrieval. Defaults to None.

    Returns:
        BarSet: Historical dataset
    """
    log.info("Calling get_stock_bars")
    
    all_symbol_data = {}
    for symbol in symbols:
        symbol_data = client.get_stock_bars(
            request_params=StockBarsRequest(
                symbol_or_symbols=symbol,
                start=start,
                end=end,
                limit=None,
                timeframe=timeframe,
                adjustment=Adjustment.ALL,
            )
        )
        all_symbol_data.update(
            symbol_data
        )
    
    return all_symbol_data
