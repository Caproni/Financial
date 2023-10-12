#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import datetime

from ..brokerage.alpaca.client.create_market_data_client import create_historical_stock_data_client
from ..brokerage.alpaca.data.get_stock_bars import get_stock_bars

def test_get_stock_bars():
    client = create_historical_stock_data_client()
    bars = get_stock_bars(
        client=client,
        symbols=["AAPL"],
        timeframe=TimeFrame(
            amount=1,
            unit=TimeFrameUnit.Day,
        ),
        start=datetime(2023, 1, 1),
        end=datetime(2023, 1, 8),
    )

    assert bars.get("AAPL") is not None
    assert len(bars.get("AAPL")) == 4
    assert bars.get("AAPL")[0].close == 124.36
