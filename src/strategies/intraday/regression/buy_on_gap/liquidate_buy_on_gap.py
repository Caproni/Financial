#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.broker.client import BrokerClient
from alpaca.trading.client import TradingClient
from alpaca.trading.models import Clock
from datetime import timedelta

from src.brokerage.alpaca.broker.get_clock import get_clock
from src.strategies.intraday.common.close_positions_conditionally import (
    close_positions_conditionally,
)
from src.utils import log


def liquidate_buy_on_gap(
    clock: Clock,
    broker_client: BrokerClient,
    trading_client: TradingClient,
):
    log.function_call()

    rest_period = (timedelta(minutes=15),)

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
