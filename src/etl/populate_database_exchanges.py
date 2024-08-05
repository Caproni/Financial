#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from src.brokerage.polygon import (
    create_client,
    get_exchanges,
)
from src.sql import create_sql_client, unpack_simple_table, insert_data, Exchanges
from src.utils import log


def populate_database_exchanges() -> bool:
    log.function_call()

    polygon_client = create_client()
    database_client = create_sql_client()

    exchanges = get_exchanges(polygon_client)

    log.info(f"Obtained: {len(exchanges)} exchanges.")

    documents = unpack_simple_table(
        collection=Exchanges,
        data=exchanges,
    )

    return insert_data(
        database_client,
        documents=documents,
    )
