#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.broker.client import BrokerClient

from src.utils.logger import logger as log


def get_account(
    client: BrokerClient,
):
    log.info("Calling get_account")
    return client.get_account()
