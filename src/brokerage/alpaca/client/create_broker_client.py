#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.broker.client import BrokerClient
from dotenv import load_dotenv
from os import getenv

from src.utils import log


def create_broker_client(
    sandbox: bool = True,
) -> BrokerClient:
    log.function_call()
    load_dotenv()
    return BrokerClient(
        api_key=(
            getenv("ALPACA_BROKER_SANDBOX_KEY")
            if sandbox
            else getenv("ALPACA_BROKER_LIVE_KEY")
        ),
        secret_key=(
            getenv("ALPACA_BROKER_SANDBOX_SECRET")
            if sandbox
            else getenv("ALPACA_BROKER_LIVE_SECRET")
        ),
        sandbox=sandbox,
    )
