#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from polygon import RESTClient
from dotenv import load_dotenv
from os import getenv

from src.utils import log


def create_client() -> RESTClient:
    log.function_call()

    load_dotenv()

    try:
        return RESTClient(api_key=getenv("POLYGON_API_KEY"))
    except Exception as e:
        log.warning("Could not create Polygon.io client")
        raise e
