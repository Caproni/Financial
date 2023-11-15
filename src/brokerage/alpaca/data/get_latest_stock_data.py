#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest

from src.utils import log


def get_latest_stock_data(
    historical_stock_client: StockHistoricalDataClient,
    symbols: list[str],
):
    log.info("Calling get_latest_stock_data")

    pagination_limit = 2000
    current = 0
    latest_stock_data = {}
    while current < len(symbols):
        latest_stock_data.update(
            historical_stock_client.get_stock_latest_quote(
                StockLatestQuoteRequest(
                    symbol_or_symbols=[
                        s.replace("/", "")
                        for s in symbols[
                            current : min(current + pagination_limit, len(symbols))
                        ]
                    ]
                )
            )
        )
        current = min(current + pagination_limit, len(symbols))

    return latest_stock_data
