#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from src.etl import (
    populate_database_stock_financials,
)
from src.utils import log


if __name__ == "__main__":

    log.info("Starting database population for stock financials.")

    populate_database_stock_financials()

    log.info("Completed database population for stock financials.")
