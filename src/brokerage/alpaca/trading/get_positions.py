#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient
from alpaca.trading.models import Position

from src.utils import log


def get_positions(
    client: TradingClient,
) -> list[Position]:
    log.function_call()

    try:
        return client.get_all_positions()
    except Exception as e:
        log.critical(f"{e}")
        raise e
