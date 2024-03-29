#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.broker.client import BrokerClient
from requests.exceptions import ConnectionError

from src.utils import log


def get_account(
    client: BrokerClient,
):
    log.info("Calling get_account")
    return client.get_account()
