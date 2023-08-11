#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest

from src.utils.logger import logger as log


def get_historical_data(
    historical_data_client: StockHistoricalDataClient,
    symbols: list[str],
):
    log.info("Calling get_historical_data")
    
    historical_data_client.get_stock_bars(
        StockBarsRequest(
            symbol_or_symbols=symbols,
            start (Optional[datetime]): The beginning of the time interval for desired data. Timezone naive inputs assumed to be in UTC.
            end (Optional[datetime]): The end of the time interval for desired data. Defaults to now. Timezone naive inputs assumed to be in UTC.
            limit=None,
            adjustment (Optional[Adjustment]): The type of corporate action data normalization.
            feed (Optional[DataFeed]): The stock data feed to retrieve from.
        )
    )