#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.broker.client import BrokerClient
from time import sleep
from datetime import timedelta

from src.strategies.intraday.regression.buy_on_gap import prepare_buy_on_gap
from src.strategies.intraday.regression.buy_on_gap import liquidate_buy_on_gap
from src.strategies.intraday.regression.buy_on_gap import trade_buy_on_gap
from src.brokerage.alpaca.broker.get_clock import get_clock
from src.utils import log


def run_buy_on_gap(
    trading_client: TradingClient,
    data_client: StockHistoricalDataClient,
    broker_client: BrokerClient,
) -> None:
    log.function_call()

    rest_period = timedelta(minutes=15)

    clock = get_clock(broker_client)

    log.info(f"Current market time: {clock.timestamp}")

    bog_data = prepare_buy_on_gap(
        clock=clock,
        trading_client=trading_client,
        data_client=data_client,
    )

    cash = float(trading_client.get_account().cash)

    trades = trade_buy_on_gap(
        cash=cash,
        strategy_data=bog_data,
        backtest_mode=False,
        trading_client=trading_client,
    )

    log.info(f"A total of {len(trades)} have been placed.")

    log.info("Updating clock...")

    clock = get_clock(broker_client)

    log.info(f"Current market time: {clock.timestamp}")

    log.info("Sleeping until market close...")

    minutes_until_next_period = (rest_period.seconds // 60) - clock.timestamp.minute % (
        rest_period.seconds // 60
    )
    sleep(minutes_until_next_period * 60)

    log.info("Updating clock...")

    clock = get_clock(broker_client)

    liquidate_buy_on_gap(
        clock=clock,
        broker_client=broker_client,
        trading_client=trading_client,
    )
