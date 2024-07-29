#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from src.etl import (
    populate_database_exchanges,
    populate_database_tickers,
    populate_database_related_companies,
)
from src.utils import log


if __name__ == "__main__":

    log.info("Starting database population.")

    # reference data

    exchanges_result = populate_database_exchanges()
    tickers_result = populate_database_tickers()
    related_companies_result = populate_database_related_companies()

    log.info("Completed database population.")
