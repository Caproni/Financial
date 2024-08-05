#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any

from src.utils import log


def unpack_simple_table(
    collection: Any,
    data: list[dict[str, Any]],
) -> list[Any]:
    log.function_call()

    documents: list[collection] = []
    for datum in data:
        dto = collection()
        for key, value in datum.items():
            if isinstance(value, list):
                for v in value:
                    setattr(dto, key, v)
            else:
                setattr(dto, key, value)
        documents.append(dto)

    return documents
