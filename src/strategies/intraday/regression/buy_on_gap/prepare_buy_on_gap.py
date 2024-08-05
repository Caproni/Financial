#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.models import Asset
from alpaca.trading.models import Clock
from alpaca.trading.client import TradingClient
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.models import BarSet
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import datetime, timedelta, timezone
from statistics import stdev
from time import sleep

from src.brokerage.alpaca.trading.get_assets import get_assets
from src.brokerage.alpaca.data import get_latest_stock_data
from src.brokerage.alpaca.data import get_stock_bars
from src.utils import log


def prepare_buy_on_gap(
    clock: Clock,
    trading_client: TradingClient,
    data_client: StockHistoricalDataClient,
    short_lookback_days: int = 20,
    long_lookback_days: int = 90,
    market_lock_threshold: float = 0.00000001,
    market_illiquidity_threshold: float = 10.0,
    low_price_threshold: float = 5.0,
) -> dict[str, float]:
    """Obtains data required for the buy on gap model.

    Args:
        clock (Clock): An Alpaca clock indicating current market time.
        trading_client (TradingClient): An Alpaca trading client.
        data_client (StockHistoricalDataClient): An Alpaca data client.
        short_lookback_days (int, optional): A short lookback period in days used to specify certain model parameters. Defaults to 20.
        long_lookback_days (int, optional): A long lookback period in days used to specify certain model parameters. Defaults to 90.
        market_lock_threshold (float, optional): A threshold for market lock.
            If the difference between bid/offer price is less than this threshold then the market for that symbol
            is considered locked and trading is not considered for it. Defaults to 0.00000001.
        market_illiquidity_threshold (float, optional): A threshold for illiquidity.
            If the difference between bid/offer price is greater than this threshold then the symbol is
            considered illiquid and trading is not considered for it. Defaults to 10.0.
        low_price_threshold (float, optional): Threshold for low price symbols. If the latest VWAP is below this threshold then trading will not be considered for that symbols. Defaults to 5.0.

    Returns:
        dict[str, float]: Data used in the buy on gap model
    """
    log.function_call()

    log.info("Getting symbols...")

    symbols: list[Asset] = get_assets(
        trading_client,
        asset_class="us_equity",
    )

    filtered_symbols: list[Asset] = []
    for s in symbols:
        if s.tradable and s.status:
            filtered_symbols.append(s)

    log.info("Filter out low price and illiquid stocks...")

    last_trade = get_latest_stock_data(
        data_client,
        sorted([s.symbol for s in filtered_symbols]),
    )

    liquid_symbols: list[Asset] = []
    for s in filtered_symbols:
        if s.symbol in last_trade.keys():
            ask_price = last_trade.get(s.symbol).ask_price
            bid_price = last_trade.get(s.symbol).bid_price
            if ask_price <= 0:
                continue
            bid_ask_spread = ask_price - bid_price
            bid_ask_spread_percentage = bid_ask_spread / ask_price * 100
            mid_price = (ask_price + bid_price) / 2
            if (
                bid_ask_spread_percentage > market_lock_threshold
                and bid_ask_spread_percentage < market_illiquidity_threshold
                and mid_price > low_price_threshold
            ):
                liquid_symbols.append(s)

    log.info(
        f"{len(liquid_symbols)} of {len(filtered_symbols)} symbols are considered liquid enough for trading."
    )

    log.info("Getting historical data...")

    long_day_bars = get_stock_bars(
        client=data_client,
        symbols=[s.symbol for s in liquid_symbols],
        timeframe=TimeFrame(
            amount=1,
            unit=TimeFrameUnit.Day,
        ),
        start=clock.timestamp - (timedelta(days=long_lookback_days)),
        end=None,
    )

    log.info("Calculating metrics...")

    short_lookback_threshold = datetime.now(tz=timezone.utc) - timedelta(
        days=short_lookback_days
    )

    short_day_bars: dict[str, BarSet] = {}
    for symbol, bars in long_day_bars.items():
        short_day_bars[symbol] = [
            bar for bar in bars if bar.timestamp >= short_lookback_threshold
        ]
    short_moving_averages: dict[str, float] = {}
    for symbol, bars in short_day_bars.items():
        if len(bars) > 0:
            short_moving_averages[symbol] = sum([bar.close for bar in bars]) / len(bars)

    long_sdt_devs: dict[str, float] = {}
    for symbol, bars in long_day_bars.items():
        closes = [bar.close for bar in bars]
        ctc_diffs: list[float] = []
        for i, this_close in enumerate(closes):
            if i >= 1:
                last_close = closes[i - 1]
                close_to_close = (this_close - last_close) / last_close
                ctc_diffs.append(close_to_close)
        if len(ctc_diffs) > 1:
            long_sdt_devs.update(
                {
                    symbol: stdev(ctc_diffs),
                }
            )

    log.info("Get yesterday's lows...")

    yesterday_lows: dict[str, float] = {}
    for symbol, bars in short_day_bars.items():
        yesterday_lows[symbol] = bars[-1].low

    log.info(f"Current market time: {clock.timestamp}")

    if not clock.is_open and clock.timestamp < clock.next_open:
        log.info(f"Market does not open until {clock.next_open}. Sleeping until then.")

        sleep((clock.next_open - clock.timestamp).seconds)

    log.info("Market is open. Getting open prices...")

    today_bars = get_stock_bars(
        data_client,
        [s.symbol for s in liquid_symbols],
        timeframe=TimeFrame(
            amount=1,
            unit=TimeFrameUnit.Day,
        ),
        start=clock.timestamp
        - (timedelta(days=3 if clock.timestamp.weekday() == 0 else 1)),
        end=None,
    )

    today_open_prices: dict[str, float] = {}
    for symbol, bars in today_bars.items():
        today_open_prices[symbol] = bars[-1].open

    bog_data: dict[str, float] = {}
    for s in today_open_prices.keys():
        bog_data[s] = {
            "today_open_prices": today_open_prices.get(s),
            "long_sdt_devs": long_sdt_devs.get(s),
            "short_moving_averages": short_moving_averages.get(s),
            "yesterday_lows": yesterday_lows.get(s),
        }

    return bog_data
