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
from alpaca.common.exceptions import APIError
from datetime import datetime

from src.utils import log


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
    log.function_call()

    all_symbol_data: BarSet = {}
    for symbol in symbols:
        try:
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
            all_symbol_data.update(symbol_data.data)
        except AttributeError as e:
            log.warning(f"No data for symbol: {symbol}. Error: {e}")
        except APIError as e:
            log.warning(f"Symbol not recognized: {symbol}. Error: {e}")

    return all_symbol_data
