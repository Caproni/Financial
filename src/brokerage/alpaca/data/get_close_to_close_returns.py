#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import datetime

from .get_stock_bars import get_stock_bars
from ....utils.logger import logger as log


def get_close_to_close_returns(
    client: StockHistoricalDataClient,
    symbols: list[str],
    start: datetime,
    end: datetime,
) -> dict[str, list[float]]:
    log.function_call()
    stock_bars = get_stock_bars(
        client=client,
        symbols=symbols,
        timeframe=TimeFrame(
            amount=1,
            unit=TimeFrameUnit.Day,
        ),
        start=start,
        end=end,
    )

    ctc_returns: dict[str, list[float]] = {}
    for symbol, bars in stock_bars.items():
        closes = [bar.close for bar in bars]
        ctc_diffs = []
        for i, this_close in enumerate(closes):
            if i >= 1:
                last_close = closes[i - 1]
                close_to_close = (this_close - last_close) / last_close
                ctc_diffs.append(close_to_close)
        ctc_returns.update(
            {
                symbol: ctc_diffs,
            }
        )

    return ctc_returns
