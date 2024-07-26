#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv

from src.utils import log


def create_mongo_client(
    mongo_uri: str | None = None,
) -> MongoClient:
    """Creates a Mongo client.

    Args:
        mongo_uri (str | None, optional): A MongoDb URI. Must contain username and password where required to connect. Defaults to None.

    Raises:
        ValueError: _description_

    Returns:
        MongoClient: A Mongo client ready to use.
    """
    log.info("Calling create_mongo_client")
    load_dotenv()

    if mongo_uri is None:
        mongo_uri = getenv("MONGO_URI")

    if not mongo_uri:
        raise ValueError("MONGO_URI must be set in the environment variables")

    return MongoClient(
        mongo_uri,
        maxPoolSize=50,
        minPoolSize=10,
        waitQueueTimeoutMS=10000,
    )
