#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from dotenv import load_dotenv
from os import getenv
from alpaca.data.historical import StockHistoricalDataClient, CryptoHistoricalDataClient
from alpaca.data.live import StockDataStream, CryptoDataStream

from src.utils.logger import logger as log


def create_historical_stock_data_client() -> StockHistoricalDataClient:
    log.info("Calling create_historical_stock_data_client")
    load_dotenv()
    return StockHistoricalDataClient(
        api_key=getenv("ALPACA_LIVE_KEY"),
        secret_key=getenv("ALPACA_LIVE_SECRET"),
    )


def create_live_stock_data_client() -> StockDataStream:
    log.info("Calling create_live_stock_data_client")
    load_dotenv()
    return StockDataStream(
        api_key=getenv("ALPACA_LIVE_KEY"),
        secret_key=getenv("ALPACA_LIVE_SECRET"),
    )


def create_historical_crypto_data_client() -> CryptoHistoricalDataClient:
    log.info("Calling create_historical_crypto_data_client")
    load_dotenv()
    return CryptoHistoricalDataClient(
        api_key=getenv("ALPACA_LIVE_KEY"),
        secret_key=getenv("ALPACA_LIVE_SECRET"),
    )


def create_live_crypto_data_client() -> CryptoDataStream:
    log.info("Calling create_live_crypto_data_client")
    load_dotenv()
    return CryptoDataStream(
        api_key=getenv("ALPACA_LIVE_KEY"),
        secret_key=getenv("ALPACA_LIVE_SECRET"),
    )
