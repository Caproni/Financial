#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from datetime import timedelta
from time import sleep
from math import floor
from alpaca.trading.enums import OrderType
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.trading.client import TradingClient
from alpaca.broker.client import BrokerClient
from alpaca.data.live.stock import StockDataStream
from alpaca.data.historical.stock import StockHistoricalDataClient

from src.brokerage.alpaca.broker.get_clock import get_clock
from src.brokerage.alpaca.data.get_latest_stock_data import get_latest_stock_data
from src.brokerage.alpaca.data.get_snapshots import get_snapshots
from src.brokerage.alpaca.data.get_stock_bars import get_stock_bars
from src.brokerage.alpaca.trading.submit_order import submit_order
from src.brokerage.alpaca.trading.get_assets import get_assets
from src.brokerage.alpaca.trading.get_positions import get_positions
from src.brokerage.alpaca.trading.get_orders import get_orders
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from src.univariate.analysis.calc_maximum_drawdown_value import (
    calc_maximum_drawdown_value,
)
from src.univariate.analysis.calc_maximum_drawdown_duration import (
    calc_maximum_drawdown_duration
)
from src.strategies.intraday.common.close_positions_conditionally import (
    close_positions_conditionally,
)
from src.brokerage.alpaca.trading.close_position import close_position
from src.strategies.common.calc_kelly_bet import calc_kelly_bet
from src.utils.logger import logger as log


def runner(
    trading_client: TradingClient,
    broker_client: BrokerClient,
    live_stock_client: StockDataStream,
    historical_stock_client: StockHistoricalDataClient,
):
    """A strategy runner

    Args:
        trading_client (TradingClient): An Alpaca trading client
        broker_client (BrokerClient): An Alpaca broker client
        live_stock_client (StockDataStream): An Alpaca live stock client
        historical_stock_client (StockHistoricalDataClient): An Alpaca historical stock client
    """

    # declare objects

    short_timeframe = TimeFrame(
        amount=5,
        unit=TimeFrameUnit.Minute,
    )

    market_lock_threshold = 0.00000001
    market_illiquidity_threshold = 10.0
    low_price_threshold = 5.0
    volume_price_threshold = 10_000_000
    market_close_cutoff_minutes = 3
    profit_threshold_percentage = 0.15
    drawdown_threshold_percentage = 5
    drawdown_duration_threshold = timedelta(minutes=30)

    # get data

    symbols = get_assets(trading_client)
    clock = get_clock(broker_client)

    # exclude non-tradable stocks

    filtered_symbols = []
    for s in symbols:
        if s.tradable:
            filtered_symbols.append(s)

    # get prices and volumes of last trade

    last_trade = get_latest_stock_data(
        historical_stock_client,
        sorted([s.symbol for s in filtered_symbols]),
    )

    # filter out low price and illiquid stocks

    liquid_symbols = []
    for s in filtered_symbols:
        if s.symbol in last_trade.keys():
            ask_price = last_trade[s.symbol].ask_price
            bid_price = last_trade[s.symbol].bid_price
            if ask_price <= 0:
                continue
            bid_ask_spread = (ask_price - bid_price) / ask_price * 100
            mid_price = (ask_price + bid_price) / 2
            if (
                bid_ask_spread > market_lock_threshold
                and bid_ask_spread < market_illiquidity_threshold
                and mid_price > low_price_threshold
            ):
                liquid_symbols.append(s)
    
    log.info(
        f"{len(liquid_symbols)} of {len(symbols)} symbols are considered liquid enough for trading."
    )

    # filter out stocks with low volume of trade the previous trading day
    
    snapshots = get_snapshots(
        historical_stock_client,
        sorted([s.symbol for s in liquid_symbols]),
    )

    shortlist_symbols = []
    for s in liquid_symbols:
        if s.symbol in snapshots.keys():
            volume = snapshots[s.symbol].previous_daily_bar.volume
            vwap = snapshots[s.symbol].previous_daily_bar.vwap
            if volume * vwap > volume_price_threshold:
                shortlist_symbols.append(s)

    log.info(
        f"{len(shortlist_symbols)} of {len(symbols)} symbols are shortlisted for trading."
    )

    # There is variability in the number of shortlisted symbols when this function is started multiple times within the same minute

    log.info(f"Entering trading loop. Symbols:")
    for s in shortlist_symbols:
        log.info(f"{s}")

    while True:
        clock = get_clock(broker_client)
        log.info(f"Current market time: {clock.timestamp}")

        cash = float(trading_client.get_account().cash)

        if not clock.is_open and clock.timestamp + timedelta(hours=2) < clock.next_open:
            log.info(
                f"Market does not open until {clock.next_open}. Sleeping for one hour."
            )
            sleep(60 * 60)
            continue

        log.info("Checking current positions / orders")

        current_positions = get_positions(trading_client)
        current_orders = get_orders(trading_client)

        for p in current_positions:
            if float(p.change_today) > profit_threshold_percentage or float(p.change_today) < 0:
                log.info(f"Liquidating order: {p}")
                close_position(
                    trading_client,
                    p.symbol,
                )

        log.info("Obtain historical data for new orders")
        
        short_timescale_stock_history = get_stock_bars(
            historical_stock_client,
            [s.symbol for s in shortlist_symbols],
            timeframe=short_timeframe,
            start=clock.timestamp - timedelta(days=1),
            end=None,
        )

        # construct orders

        new_orders: list[MarketOrderRequest] = []
        for s in shortlist_symbols:
            short_data = short_timescale_stock_history.data[s.symbol]
            maximum_drawdown_value_percentage = calc_maximum_drawdown_value(
                data=[d.vwap for d in short_data],
            )["maximum_drawdown_value_percentage"]
            mdd_duration = calc_maximum_drawdown_duration(
                data=[d.vwap for d in short_data],
                ts=[d.timestamp for d in short_data],
            )
            mdd_delta = mdd_duration["maximum_drawdown_duration_end_timestamp"] - mdd_duration["maximum_drawdown_duration_start_timestamp"]
            if maximum_drawdown_value_percentage < drawdown_threshold_percentage and mdd_delta < drawdown_duration_threshold:
                qty = floor(
                    cash * min(1, calc_kelly_bet(
                            p_win=0.6,
                            win_loss_ratio=1.1,
                        ),
                    )
                    / 2 / snapshots[s.symbol].latest_quote.ask_price)
                side = OrderSide.BUY
                order_type = OrderType.MARKET
                if qty < 0:
                    if not (s.shortable and s.easy_to_borrow):
                        continue
                    side = OrderSide.SELL
                    order_type = OrderType.LIMIT

                new_orders.append(
                    MarketOrderRequest(
                        symbol=s.symbol,
                        qty=abs(qty),
                        side=side,
                        type=order_type,
                        time_in_force=TimeInForce.DAY,
                    )
                )

        # submit orders

        if clock.is_open and clock.timestamp + timedelta(minutes=market_close_cutoff_minutes) < clock.next_close:
            for new_order in new_orders:
                log.info(f"Submitting order for {new_order.qty} shares of: {s}")
                try:
                    submit_order(
                        trading_client,
                        symbol=new_order.symbol,
                        quantity=new_order.qty,
                        side=new_order.side,
                        order_type=new_order.type,
                        time_in_force=new_order.time_in_force,
                    )
                    log.info(f"Submitted order for {new_order.qty} shares of: {s}")
                except Exception as e:
                    log.error(f"Could not submit order. Error: {e}")
                    continue

        close_positions_conditionally(
            broker_client=broker_client,
            trading_client=trading_client,
            within=timedelta(minutes=market_close_cutoff_minutes),
        )
