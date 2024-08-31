#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os import getenv
import sentry_sdk
from dotenv import load_dotenv

from src.etl import (
    populate_database_stock_financials,
)
from src.utils import log

load_dotenv()

sentry_sdk.init(
    dsn=getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

if __name__ == "__main__":

    log.info("Starting database population for stock financials.")

    populate_database_stock_financials()

    log.info("Completed database population for stock financials.")
