#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any

from src.sql.dto import RelatedCompanies
from src.utils import log


def unpack_related_companies(data: list[dict[str, Any]]) -> list[RelatedCompanies]:
    log.function_call()

    documents: list[RelatedCompanies] = []
    for datum in data:
        if datum["tickers"] is not None:
            for t in datum["tickers"]:
                documents.append(
                    RelatedCompanies(
                        symbol=datum["symbol"],
                        ticker=t,
                    )
                )

    return documents
