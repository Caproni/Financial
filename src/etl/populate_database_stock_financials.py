#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from src.brokerage.polygon import (
    create_polygon_client,
    get_stock_financials,
)
from src.sql import create_sql_client, insert_data, get_data, Tickers
from src.sql.func import unpack_stock_financials
from src.utils import log


def populate_database_stock_financials() -> bool:
    """
    Populates the database with stock financial information.

    Returns:
        A boolean value indicating the success of data population for stock financials.
    """
    log.function_call()

    polygon_client = create_polygon_client()
    database_client = create_sql_client()

    tickers = get_data(
        database_client,
        models=[Tickers],
    )

    N = len(tickers)

    results: list = []
    for i, ticker in enumerate(tickers):
        log.info(f"Processing ticker {i + 1} of {N}")
        log.info(f"Processing: {ticker['ticker']}")

        if stock_financials := get_stock_financials(
            client=polygon_client,
            ticker=ticker["ticker"],
        ):
            log.info(f"Obtained: {len(stock_financials)} stock financials.")

            financial_reporting_item_documents, financial_documents = (
                unpack_stock_financials(
                    data=stock_financials,
                )
            )

            if financial_result := insert_data(
                database_client,
                documents=financial_documents,
            ):
                financial_reporting_item_result = insert_data(
                    database_client,
                    documents=financial_reporting_item_documents,
                )

                results.append((financial_result, financial_reporting_item_result))

    return results
