#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from os.path import dirname, join, abspath

from src.backtesting.data import load_historical_data
from src.strategies.intraday.regression.buy_on_gap import run_buy_on_gap
from src.backtesting.backtest_intraday_strategy import backtest_intraday_strategy


def test_backtest_intraday_strategy():
    data_path = abspath(join(dirname(__file__), "assets/json", "daily_data.json"))
    data = load_historical_data(...)
    backtest_intraday_strategy(
        data=data,
        strategy=run_buy_on_gap,
    )
