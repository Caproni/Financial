#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from polygon import RESTClient
from dotenv import load_dotenv
from os import getenv

from src.utils import log

def get_symbols():
    log.info("Calling get_symbols")
    
    load_dotenv()
    
    return RESTClient(api_key=getenv("POLYGON_API_KEY")).list_tickers()