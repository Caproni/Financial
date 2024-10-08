#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from polygon import RESTClient
from datetime import datetime

from src.utils import log


def list_ticker_news(
    client: RESTClient,
    ticker: str | None = None,
    published_utc_gte: datetime | None = None,
    published_utc_lt: datetime | None = None,
    raw: bool = True,
) -> list[dict[str, Any]]:
    """Obtains news articles within a time range and optionally for a specific ticker.

    Args:
        client (RESTClient): A Polygon client.
        ticker (str | None, optional): Optionally, a ticker for which to obtain news. Defaults to None.
        published_utc_gte (datetime | None, optional): Lower time bound for news articles. Defaults to None.
        published_utc_lt (datetime | None, optional): Upper time bound for news articles. Defaults to None.
        raw (bool, optional): Whether to return a raw data payload. Defaults to True.

    Returns:
        list[dict[str, Any]]: A list of obtained news articles.
    """
    log.function_call()

    try:
        response = client.list_ticker_news(
            ticker=ticker,
            published_utc_lt=published_utc_lt.isoformat(),
            published_utc_gte=published_utc_gte.isoformat(),
            raw=raw,
            limit=1_000,
        )
    except Exception as e:
        log.error(f"Error: {e}")
        return []

    if raw:
        results = response.json()["results"]
        return [
            {
                "amp_url": e["amp_url"] if "amp_url" in e.keys() else None,
                "article_url": e["article_url"] if "article_url" in e.keys() else None,
                "author": e["author"] if "author" in e.keys() else None,
                "description": e["description"] if "description" in e.keys() else None,
                "polygon_id": e["id"] if "id" in e.keys() else None,
                "image_url": e["image_url"] if "image_url" in e.keys() else None,
                "keywords": e["keywords"] if "keywords" in e.keys() else None,
                "published_utc": (
                    datetime.fromisoformat(e["published_utc"])
                    if "published_utc" in e.keys()
                    else None
                ),
                "publisher": {
                    "favicon_url": (
                        e["publisher"]["favicon_url"]
                        if "publisher" in e.keys()
                        else None
                    ),
                    "homepage_url": (
                        e["publisher"]["homepage_url"]
                        if "publisher" in e.keys()
                        else None
                    ),
                    "logo_url": (
                        e["publisher"]["logo_url"] if "publisher" in e.keys() else None
                    ),
                    "name": e["publisher"]["name"] if "publisher" in e.keys() else None,
                },
                "tickers": e["tickers"] if "tickers" in e.keys() else None,
                "title": e["title"] if "title" in e.keys() else None,
                "insights": e["insights"] if "insights" in e.keys() else None,
            }
            for e in results
        ]

    return [
        {
            "amp_url": e.amp_url,
            "article_url": e.article_url,
            "author": e.author,
            "description": e.description,
            "polygon_id": e.id,
            "image_url": e.image_url,
            "keywords": e.keywords,
            "published_utc": datetime.fromisoformat(e.published_utc),
            "publisher": {
                "favicon_url": e.publisher.favicon_url,
                "homepage_url": e.publisher.homepage_url,
                "logo_url": e.publisher.logo_url,
                "name": e.publisher.name,
            },
            "tickers": e.tickers,
            "title": e.title,
        }
        for e in response
    ]
