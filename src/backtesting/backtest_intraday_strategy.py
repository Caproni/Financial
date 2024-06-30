#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from typing import Any, Callable
from alpaca.trading.enums import OrderSide
from datetime import datetime, timedelta, timezone
from statistics import stdev
import matplotlib.pyplot as plt

from src.utils import log


def backtest_intraday_strategy(
    data: dict[str, list[str, Any]],
    strategy: Callable,
    starting_cash: float,
) -> dict[str, Any]:
    """Performs backtesting of the supplied strategy in the context of supplied data. Assumes that the strategy will be traded intraday, so that all positions will be closed at end of day.

    Warning: Ensure that the data resolution and trading universe are compatible with the supplied strategy

    Args:
        data (dict[str, list[str, Any]]): Historical trading data
        strategy (Callable): A strategy to test

    Returns:
        dict[str, Any]: A results set indicating the performance of the strategy
    """
    log.info("Calling backtest_intraday_strategy")

    universe = list(data.keys())
    start_datetime = datetime(2999, 1, 1, tzinfo=timezone.utc)
    end_datetime = datetime(1951, 5, 16, tzinfo=timezone.utc)

    short_lookback_days: int = 20
    long_lookback_days: int = 90

    log.info(f"Universe contains: {len(universe)} symbols")

    # get strategy specific data

    for s, symbol_data in data.items():  # assume symbol data is time-ordered
        start_datetime = min(start_datetime, symbol_data[0]["timestamp"])
        end_datetime = max(end_datetime, symbol_data[-1]["timestamp"])

    log.info(f"Backtest trading window starts at: {start_datetime}")
    log.info(f"Backtest trading window ends at: {end_datetime}")

    trades: dict[datetime, list[dict[str, Any]]] = {}
    cash = starting_cash
    strategy_data: dict[datetime, dict[str, float]] = {}
    price_data: dict[datetime, dict[str, float]] = {}
    day = start_datetime + timedelta(days=long_lookback_days)
    daily_cash: list[float] = [cash]
    daily_date: list[datetime] = [day]
    while day < end_datetime:
        log.info(f"Current date: {day}")
        log.info(f"Current cash: {cash}")
        short_lookback_threshold = day - timedelta(days=short_lookback_days)
        long_lookback_threshold = day - timedelta(days=long_lookback_days)
        strategy_data_payload: dict[str, float] = {}
        price_data_payload: dict[str, float] = {}
        for s, symbol_data in data.items():
            yesterday_data = []
            days_offset = 0
            while not yesterday_data and days_offset < long_lookback_days:
                days_offset += 1
                yesterday_data = [
                    d
                    for d in symbol_data
                    if d["timestamp"].year == (day - timedelta(days=days_offset)).year
                    and d["timestamp"].month
                    == (day - timedelta(days=days_offset)).month
                    and d["timestamp"].day == (day - timedelta(days=days_offset)).day
                ]
            today_data = [
                d
                for d in symbol_data
                if d["timestamp"].year == day.year
                and d["timestamp"].month == day.month
                and d["timestamp"].day == day.day
            ]
            long_lookback_closes = [
                d["close"]
                for d in symbol_data
                if d["timestamp"] >= long_lookback_threshold and d["timestamp"] < day
            ]
            short_lookback_closes = [
                d["close"]
                for d in symbol_data
                if d["timestamp"] >= short_lookback_threshold and d["timestamp"] < day
            ]
            ctc_diffs: list[float] = []
            for i, this_close in enumerate(long_lookback_closes):
                if i >= 1:
                    last_close = long_lookback_closes[i - 1]
                    close_to_close = (this_close - last_close) / last_close
                    ctc_diffs.append(close_to_close)
            if (
                today_data
                and yesterday_data
                and short_lookback_closes
                and len(ctc_diffs) > 1
            ):
                strategy_data_payload[s] = {
                    "long_sdt_devs": stdev(ctc_diffs),
                    "short_moving_averages": sum(short_lookback_closes)
                    / len(short_lookback_closes),
                    "yesterday_lows": yesterday_data[0]["low"],
                    "today_open_prices": today_data[0]["open"],
                }
                price_data_payload[s] = {
                    "today_close_prices": today_data[0]["close"],
                }
        if strategy_data_payload:
            strategy_data[day] = strategy_data_payload
        if price_data_payload:
            price_data[day] = price_data_payload

        # run strategy

        daily_data = strategy_data.get(day)
        if daily_data is not None:
            trades[day] = strategy(
                cash=cash,
                strategy_data=daily_data,
                backtest_mode=True,
            )

            # evaluate profit

            profit = 0
            for trade in trades[day]:
                today_close_prices = price_data_payload[trade["symbol"]][
                    "today_close_prices"
                ]
                multiplier = 1 if trade["side"] == OrderSide.BUY else -1
                profit += (
                    trade["quantity"]
                    * (today_close_prices - trade["price"])
                    * multiplier
                )

            cash += profit
            daily_cash.append(cash)
            daily_date.append(day)

        day += timedelta(days=1)

    plt.plot(daily_date, daily_cash)
    plt.show()
