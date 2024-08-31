#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os import getenv
import sentry_sdk
from dotenv import load_dotenv

from src.etl import (
    populate_database_exchanges,
    populate_database_tickers,
    populate_database_related_companies,
)
from src.utils import log

load_dotenv()

sentry_sdk.init(
    dsn=getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

if __name__ == "__main__":

    log.info("Starting database population.")

    # reference data

    exchanges_result = populate_database_exchanges()
    tickers_result = populate_database_tickers()
    related_companies_result = populate_database_related_companies()

    log.info("Completed database population.")
