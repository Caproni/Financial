#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from datetime import datetime

from ..brokerage.alpaca.client.create_market_data_client import (
    create_historical_stock_data_client,
)
from ..brokerage.alpaca.data.get_close_to_close_returns import (
    get_close_to_close_returns,
)


def test_get_close_to_close_returns():
    client = create_historical_stock_data_client()
    ctc_returns = get_close_to_close_returns(
        client=client,
        symbols=["AAPL"],
        start=datetime(2023, 1, 1),
        end=datetime(2023, 1, 8),
    )

    assert ctc_returns.get("AAPL") is not None
    assert len(ctc_returns.get("AAPL")) == 3
    assert ctc_returns.get("AAPL")[0] == 0.010373110324863351
