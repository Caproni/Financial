#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from typing import Any
from alpaca.trading.client import TradingClient
from alpaca.trading.models import Asset
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
from math import floor

from src.brokerage.alpaca.trading.submit_order import submit_order
from src.utils import log


def trade_buy_on_gap(
    cash: float,
    strategy_data: dict[str, dict[str, float]],
    backtest_mode: bool = True,
    trading_client: TradingClient | None = None,
) -> list[dict[str, Any]]:
    """Trade the buy on gap strategy. This is an intra-day regression strategy which takes both long and short positions
    conditionally at the start of the trading day based on a gap approach.
    This function should be ran on/shortly after the start of the trading day.

    Args:
        cash (float): Current amount of cash in trading currency
        strategy_data (dict[str, dict[str, float]]): Stock data on which to run the strategy. Keys are trading symbols.
        backtest_mode (bool): Indicates whether the trading and data clients should be used.
        trading_client (TradingClient, None): An alpca trading client. Only provided when not in backtest mode. Defaults to None.
    Returns:
        list[dict[str, float]]: A list of trades made by this strategy
    """
    log.info("Calling trade_buy_on_gap")

    if not backtest_mode:
        assert (
            trading_client is not None
        ), "A trading client must be provided when not using backtest mode"

    for k, v in strategy_data.items():
        assert (
            v.get("today_open_prices") is not None
        ), f"Today open prices data is not available for symbol: {k}"
        assert (
            v.get("yesterday_lows") is not None
        ), f"Yesterday's lows prices data is not available for symbol: {k}"
        assert (
            v.get("short_moving_averages") is not None
        ), f"Short period moving average data is not available for symbol: {k}"
        assert (
            v.get("long_sdt_devs") is not None
        ), f"Long period std deviations data is not available for symbol: {k}"

    max_stocks_to_take_long_position: int = 10
    max_stocks_to_take_short_position: int = 10

    log.info("Selecting stocks...")

    selected_gapped_down_stocks: list[Asset] = []
    selected_gapped_down_stock_returns: list[float] = []
    selected_gapped_up_stocks: list[Asset] = []
    selected_gapped_up_stock_returns: list[float] = []
    for symbol, data in strategy_data.items():
        log.info(f"Processing: {symbol}")
        today_open = data["today_open_prices"]
        yesterday_low = data["yesterday_lows"]
        average = data["short_moving_averages"]
        sd = data["long_sdt_devs"]
        if (
            today_open is not None
            and yesterday_low is not None
            and yesterday_low is not None
            and average is not None
        ):
            gap = (
                yesterday_low - today_open
            ) / today_open  # positive when gapped down, negative when gapped up
            if (
                gap > sd and today_open > average
            ):  # seeking stocks which gap down more than a specific amount and whose prices are currently trending high
                selected_gapped_down_stocks.append(symbol)
                selected_gapped_down_stock_returns.append(gap)
            if (
                gap < -sd and today_open < average
            ):  # seeking stocks which gap up more than a specific amount and whose prices are currently trending low
                selected_gapped_up_stocks.append(symbol)
                selected_gapped_up_stock_returns.append(-gap)

    selected_gapped_down_stocks = [
        x
        for _, x in sorted(
            zip(selected_gapped_down_stock_returns, selected_gapped_down_stocks)
        )
    ]
    selected_gapped_up_stocks = [
        x
        for _, x in sorted(
            zip(selected_gapped_up_stock_returns, selected_gapped_up_stocks)
        )
    ]

    if len(selected_gapped_down_stocks) > max_stocks_to_take_long_position:
        selected_gapped_down_stocks = selected_gapped_down_stocks[
            0:max_stocks_to_take_long_position
        ]

    if len(selected_gapped_up_stocks) > max_stocks_to_take_short_position:
        selected_gapped_up_stocks = selected_gapped_up_stocks[
            0:max_stocks_to_take_short_position
        ]

    log.info("Purchasing stocks...")

    log.info(f"Total of: {len(selected_gapped_down_stocks)} stocks to purchase.")

    trades: list[dict[str, float]] = []
    for selected_stock in selected_gapped_down_stocks:
        price = strategy_data[selected_stock].get("today_open_prices")
        quantity = floor(
            cash
            / price
            / (len(selected_gapped_down_stocks) + len(selected_gapped_up_stocks))
        )
        log.info(f"Submitting long order for {quantity} shares of: {selected_stock}")
        try:
            if not backtest_mode:
                submit_order(
                    trading_client,
                    symbol=selected_stock,
                    quantity=quantity,
                    side=OrderSide.BUY,
                    order_type=OrderType.MARKET,
                    time_in_force=TimeInForce.DAY,
                )
            log.info(f"Submitted long order for {quantity} shares of: {selected_stock}")
            trades.append(
                {
                    "symbol": selected_stock,
                    "quantity": quantity,
                    "price": price,
                    "side": OrderSide.BUY,
                    "order_type": OrderType.MARKET,
                    "time_in_force": TimeInForce.DAY,
                }
            )
        except Exception as e:
            log.error(f"Could not submit order. Error: {e}")

    log.info(f"Total of: {len(selected_gapped_up_stocks)} stocks to short.")

    for selected_stock in selected_gapped_up_stocks:
        price = strategy_data[selected_stock].get("today_open_prices")
        quantity = floor(
            cash
            / price
            / (len(selected_gapped_down_stocks) + len(selected_gapped_up_stocks))
        )
        log.info(f"Submitting short order for {quantity} shares of: {selected_stock}")
        try:
            if not backtest_mode:
                submit_order(
                    trading_client,
                    symbol=selected_stock,
                    quantity=quantity,
                    side=OrderSide.SELL,
                    order_type=OrderType.MARKET,
                    time_in_force=TimeInForce.DAY,
                )
            log.info(
                f"Submitted short order for {quantity} shares of: {selected_stock}"
            )
            trades.append(
                {
                    "symbol": selected_stock,
                    "quantity": quantity,
                    "price": price,
                    "side": OrderSide.SELL,
                    "order_type": OrderType.MARKET,
                    "time_in_force": TimeInForce.DAY,
                }
            )
        except Exception as e:
            log.error(f"Could not submit order. Error: {e}")

    return trades
