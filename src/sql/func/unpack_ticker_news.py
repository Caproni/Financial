#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any

from src.sql.dto import TickerNews
from src.utils import log


def unpack_ticker_news(data: list[dict[str, Any]]) -> list[TickerNews]:
    log.function_call()
    
    documents: list[RelatedCompanies] = []