#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from pymongo.results import InsertManyResult

from src.brokerage.polygon import (
    create_client,
    get_exchanges,
)
from src.mongo import insert_data, delete_data, create_mongo_client
from src.utils import log


def populate_database_exchanges() -> InsertManyResult:
    log.info("Calling populate_database_exchanges")

    polygon_client = create_client()
    mongo_client = create_mongo_client()

    exchanges = get_exchanges(polygon_client)

    delete_data(
        mongo_client,
        database="financial",
        collection="exchanges",
    )

    return insert_data(
        mongo_client,
        database="financial",
        collection="exchanges",
        documents=exchanges,
    )
