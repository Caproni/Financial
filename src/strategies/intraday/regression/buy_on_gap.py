#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import OrderRequest
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
from alpaca.trading.models import Asset
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.models import BarSet
from alpaca.broker.client import BrokerClient
from time import sleep
from math import floor
from statistics import stdev
from datetime import datetime, timedelta, timezone

from src.brokerage.alpaca.broker.get_clock import get_clock
from src.brokerage.alpaca.trading.get_assets import get_assets
from src.brokerage.alpaca.data.get_latest_stock_data import get_latest_stock_data
from src.brokerage.alpaca.data.get_snapshots import get_snapshots
from src.brokerage.alpaca.data.get_stock_bars import get_stock_bars
from src.brokerage.alpaca.trading.submit_order import submit_order
from src.strategies.intraday.common.close_positions_conditionally import (
    close_positions_conditionally,
)
from src.utils.logger import logger as log


def buy_on_gap(
    trading_client: TradingClient,
    data_client: StockHistoricalDataClient,
    broker_client: BrokerClient,
) -> None:
    log.info("Calling buy_on_gap")
    
    market_lock_threshold = 0.00000001
    market_illiquidity_threshold = 10.0
    low_price_threshold = 5.0
    long_lookback_days = 90
    short_lookback_days = 20
    rest_period = timedelta(minutes=15)
    
    clock = get_clock(broker_client)
    
    log.info(f"Current market time: {clock.timestamp}")
    
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
        
    data_available_stocks = long_day_bars.keys()
            
    log.info("Calculating metrics...")
    
    short_lookback_threshold = datetime.now(tz=timezone.utc) - timedelta(days=short_lookback_days)
    
    short_day_bars: dict[str, BarSet] = {}
    for symbol, bars in long_day_bars.items():
        short_day_bars[symbol] = [bar for bar in bars if bar.timestamp >= short_lookback_threshold]
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
    
    log.info("Updating clock...")
    
    clock = get_clock(broker_client)
    
    log.info(f"Current market time: {clock.timestamp}")
    
    if not clock.is_open and clock.timestamp < clock.next_open:
        log.info(
            f"Market does not open until {clock.next_open}. Sleeping until then."
        )

        sleep((clock.next_open - clock.timestamp).seconds + 1)

    log.info("Market is open. Getting open prices...")
    
    today_bars = get_stock_bars(
        data_client,
        [s.symbol for s in liquid_symbols],
        timeframe=TimeFrame(
            amount=1,
            unit=TimeFrameUnit.Day,
        ),
        start=clock.timestamp - (timedelta(days=3 if clock.timestamp.weekday() == 0 else 1)),
        end=None,
    )
    
    today_open_prices: dict[str, float] = {}
    for symbol, bars in today_bars.items():
        today_open_prices[symbol] = bars[-1].open
    
    log.info("Selecting stocks...")
    
    selected_gapped_down_stocks: list[Asset] = []
    selected_gapped_down_stock_returns: list[float] = []
    for s in liquid_symbols:
        log.info(f"Processing: {s.symbol}")
        if s.symbol in data_available_stocks:
            today_open = today_open_prices.get(s.symbol)
            yesterday_low = yesterday_lows.get(s.symbol)
            average = short_moving_averages.get(s.symbol)
            sd = long_sdt_devs.get(s.symbol)
            if today_open is not None and yesterday_low is not None and yesterday_low is not None and average is not None:
                gap = (yesterday_low - today_open) / today_open  # positive when gapped down, negative when gapped up
                if gap > sd and today_open > average:  # seeking stocks which gap down more than a specific amount and whose prices are currently trending high
                    selected_gapped_down_stocks.append(s)
                    selected_gapped_down_stock_returns(gap)
    
    selected_gapped_down_stocks = [x for _, x in sorted(zip(selected_gapped_down_stock_returns, selected_gapped_down_stocks))]

    if len(selected_gapped_down_stocks) > 10:
        selected_gapped_down_stocks = selected_gapped_down_stocks[0:10]
    
    log.info("Updating clock...")

    clock = get_clock(broker_client)
    
    log.info("Purchasing stocks...")
        
    cash = float(trading_client.get_account().cash)
    
    snapshots = get_snapshots(
        data_client,
        sorted([s.symbol for s in selected_gapped_down_stocks]),
    )
    
    log.info(f"Total of: {len(selected_gapped_down_stocks)} stocks to purchase.")
    
    for selected_stock in selected_gapped_down_stocks:
        ask_price = snapshots.get(s.symbol).latest_quote.ask_price
        quantity = floor(cash / ask_price / len(selected_gapped_down_stocks))
        log.info(f"Submitting order for {quantity} shares of: {selected_stock.symbol}")
        try:
            submit_order(
                trading_client,
                symbol=selected_stock.symbol,
                quantity=quantity,
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                time_in_force=TimeInForce.DAY,
            )
            log.info(f"Submitted order for {quantity} shares of: {selected_stock.symbol}")
        except Exception as e:
            log.error(f"Could not submit order. Error: {e}")

    log.info("Updating clock...")
    
    clock = get_clock(broker_client)
    
    log.info(f"Current market time: {clock.timestamp}")
        
    log.info(f"Sleeping until market close...")
    
    minutes_until_next_period = (
        rest_period.seconds // 60
    ) - clock.timestamp.minute % (rest_period.seconds // 60)
    sleep(minutes_until_next_period * 60)
    
    log.info("Updating clock...")
    
    clock = get_clock(broker_client)
            
    log.info(f"Current market time: {clock.timestamp}")
    
    log.info("Liquidating stocks...")

    if clock.is_open and clock.timestamp + rest_period > clock.next_close:
        log.info("Market closing soon. Closing positions.")
        close_positions_conditionally(
            broker_client=broker_client,
            trading_client=trading_client,
            within=timedelta(minutes=rest_period.seconds // 60),
        )
    
    log.info("All positions closed. Done.")
