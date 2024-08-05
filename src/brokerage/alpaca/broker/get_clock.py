#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.broker.client import BrokerClient
from alpaca.trading.models import Clock

from src.utils import log


def get_clock(
    client: BrokerClient,
) -> Clock:
    log.function_call()

    return client.get_clock()
