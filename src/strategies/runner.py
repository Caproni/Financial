#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from datetime import timedelta
from time import sleep
from math import floor
from statistics import median, stdev
from alpaca.trading.enums import OrderType
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.trading.client import TradingClient
from alpaca.broker.client import BrokerClient
from alpaca.data.live.stock import StockDataStream
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.trading.requests import LimitOrderRequest

from src.brokerage.alpaca.broker.get_clock import get_clock
from src.brokerage.alpaca.data.get_latest_stock_data import get_latest_stock_data
from src.brokerage.alpaca.data.get_snapshots import get_snapshots
from src.brokerage.alpaca.data.get_stock_bars import get_stock_bars
from src.brokerage.alpaca.trading.submit_order import submit_order
from src.brokerage.alpaca.trading.get_assets import get_assets
from src.brokerage.alpaca.trading.get_positions import get_positions
from src.brokerage.alpaca.trading.get_orders import get_orders
from alpaca.trading.requests import OrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from src.univariate.analysis.get_drawups import get_drawups
from src.univariate.analysis.get_drawdowns import get_drawdowns
from src.univariate.analysis.calc_hurst_exponent import calc_hurst_exponent
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
        amount=15,
        unit=TimeFrameUnit.Minute,
    )

    rest_period = timedelta(minutes=15)

    market_lock_threshold = 0.00000001
    market_illiquidity_threshold = 10.0
    low_price_threshold = 5.0
    volume_price_threshold = 10_000_000
    market_close_cutoff_minutes = 3
    stdev_threshold = 0.25
    drawdown_threshold_percentage = 1
    hurst_threshold = 0.5

    log.info(f"Entering trading loop.")

    first_run = True

    while True:
        if first_run:
            # get data

            symbols = get_assets(
                trading_client,
                asset_class="us_equity",
            )

            clock = get_clock(broker_client)

            # exclude non-tradable stocks

            filtered_symbols = []
            for s in symbols:
                if s.tradable and s.status:
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
                f"{len(liquid_symbols)} of {len(symbols)} symbols are considered liquid enough for trading."
            )

            first_run = False

        clock = get_clock(broker_client)
        log.info(f"Current market time: {clock.timestamp}")

        if not clock.is_open and clock.timestamp < clock.next_open:
            log.info(
                f"Market does not open until {clock.next_open}. Sleeping until then."
            )
            sleep((clock.next_open - clock.timestamp).seconds)
            first_run = True
            continue

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

        log.info(f"Trading on symbols:")
        for s in shortlist_symbols:
            log.info(f"{s.symbol}")

        cash = float(trading_client.get_account().cash)

        log.info("Checking current positions / orders")

        current_positions = get_positions(trading_client)
        current_orders = get_orders(trading_client)

        for p in current_positions:
            log.info(f"Liquidating order: {p}")
            close_position(
                trading_client,
                p.symbol,
            )

        log.info("Obtaining historical data for new orders")

        short_timescale_stock_history = get_stock_bars(
            historical_stock_client,
            [s.symbol for s in shortlist_symbols],
            timeframe=short_timeframe,
            start=clock.timestamp - (timedelta(days=3 if clock.timestamp.weekday() == 0 else 1)),
            end=None,
        )

        # construct orders

        new_orders: list[OrderRequest] = []
        for s in shortlist_symbols:
            log.info(f"Symbol: {s}")
            short_data = short_timescale_stock_history[s.symbol]
            short_vwap = [s.vwap for s in short_data]
            last_trade = get_latest_stock_data(
                historical_stock_client,
                [s.symbol],
            )

            mid_price = (
                last_trade[s.symbol].ask_price + last_trade[s.symbol].bid_price
            ) / 2
            half_spread = (
                last_trade[s.symbol].ask_price - last_trade[s.symbol].bid_price
            ) / 2
            
            log.info(f"Midprice: {mid_price}")
            log.info(f"Spread: {2 * half_spread}")

            drawdowns = get_drawdowns(short_vwap)
            median_drawdown = median(drawdowns)

            drawups = get_drawups(short_vwap)
            median_drawup = median(drawups)
            
            log.info(f"Median drawdown: {median_drawdown}")
            log.info(f"Median drawup: {median_drawup}")

            qty = floor(
                cash
                * min(
                    1,
                    calc_kelly_bet(
                        p_win=1 - calc_hurst_exponent(short_vwap),
                        win_loss_ratio=median_drawup - median_drawdown,
                    ),
                )
                / 2
                / snapshots[s.symbol].latest_quote.ask_price
            )

            # regression / trending down
            if (
                median_drawup - median_drawdown
            ) > drawdown_threshold_percentage and stdev(
                [s.vwap for s in short_data]
            ) > stdev_threshold:
                if qty < 0 and s.easy_to_borrow and s.shortable:
                    log.info("Creating Limit Order for negative quantity")
                    new_orders.append(
                        LimitOrderRequest(
                            symbol=s.symbol,
                            qty=qty,
                            side=OrderSide.SELL,
                            type=OrderType.LIMIT,
                            time_in_force=TimeInForce.DAY,
                            limit_price=round(100 * (mid_price - 3 * half_spread / 2))
                            / 100,
                        )
                    )

            # regression / trending up
            if (
                median_drawdown - median_drawup
            ) > drawdown_threshold_percentage and stdev(
                [s.vwap for s in short_data]
            ) > stdev_threshold:
                if qty > 0:
                    log.info("Creating Limit Order for positive quantity")
                    new_orders.append(
                        LimitOrderRequest(
                            symbol=s.symbol,
                            qty=qty,
                            side=OrderSide.BUY,
                            type=OrderType.LIMIT,
                            time_in_force=TimeInForce.DAY,
                            limit_price=round(100 * (mid_price + 3 * half_spread / 2))
                            / 100,
                        )
                    )

        # submit orders

        clock = get_clock(broker_client)

        if (
            clock.is_open
            and clock.timestamp + timedelta(minutes=market_close_cutoff_minutes)
            < clock.next_close
        ):
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
                        limit_price=new_order.limit_price,
                    )
                    log.info(f"Submitted order for {new_order.qty} shares of: {s}")
                except Exception as e:
                    log.error(f"Could not submit order. Error: {e}")
                    continue

        clock = get_clock(broker_client)

        if clock.is_open:
            log.info("Sleeping until next trading period")

            if clock.timestamp + rest_period > clock.next_close:
                log.info("Market closing soon. Closing positions.")
                close_positions_conditionally(
                    broker_client=broker_client,
                    trading_client=trading_client,
                    within=timedelta(minutes=rest_period.seconds // 60),
                )

            minutes_until_next_period = (
                rest_period.seconds // 60
            ) - clock.timestamp.minute % (rest_period.seconds // 60)
            sleep(minutes_until_next_period * 60)
            continue
