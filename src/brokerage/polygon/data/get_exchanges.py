#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from polygon import RESTClient

from src.utils import log


def get_exchanges(
    client: RESTClient,
) -> None | list[dict[str, Any]]:
    """
    Retrieves the list of exchanges.

    Args:
        client: RESTClient object for making API requests.

    Returns:
        A list of exchanges, or None if an error occurs.

    Raises:
        Any exception that occurs during the API request.
    """
    log.function_call()
    try:
        response = client.get_exchanges()
    except Exception as e:
        log.error(f"Error: {e}")
        return None

    return [
        {
            "acronym": e.acronym,
            "asset_class": e.asset_class,
            "exchange_id": e.id,
            "locale": e.locale,
            "mic": e.mic,
            "name": e.name,
            "operating_mic": e.operating_mic,
            "participant_id": e.participant_id,
            "type": e.type,
            "url": e.url,
        }
        for e in response
    ]
