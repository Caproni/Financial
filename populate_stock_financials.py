#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import sentry_sdk

from src.etl import (
    populate_database_stock_financials,
)
from src.utils import log

sentry_sdk.init(
    dsn="https://8cd12a857607d331985d59a77ea0828e@o4507797009334272.ingest.de.sentry.io/4507797017133136",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

if __name__ == "__main__":

    log.info("Starting database population for stock financials.")

    populate_database_stock_financials()

    log.info("Completed database population for stock financials.")
