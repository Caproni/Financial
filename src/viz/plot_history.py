#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pymongo import MongoClient

from src.mongo import get_data
from src.utils import log


def plot_history(
    mongo_client: MongoClient,
    symbol: str,
    news_flag: bool = False,
):
    log.info("Calling plot_history")

    stocks = get_data(
        mongo_client,
        database="financial",
        collection="polygon_daily_historical_market_data",
        pipeline=[{"$match": {"symbol": symbol}}],
    )

    stocks_df = pd.DataFrame(stocks)

    stocks_df = stocks_df.sort_values("timestamp")

    news: list[dict[str, Any]] | None = None
    if news_flag:
        log.info("Obtaining news data.")
        news = get_data(
            mongo_client,
            database="financial",
            collection="ticker_news",
            pipeline=[{"$match": {"tickers": symbol}}],
        )

    news_df = pd.DataFrame(news)

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=stocks_df["timestamp"],
                open=stocks_df["open"],
                high=stocks_df["high"],
                low=stocks_df["low"],
                close=stocks_df["close"],
            )
        ]
    )

    fig.update_layout(
        title="Stock Prices with News Annotations",
        xaxis_title="Timestamp",
        yaxis_title="Stock Price",
        xaxis_rangeslider_visible=True,
    )

    sentiment_colors = {
        "positive": "green",
        "negative": "red",
        "neutral": "gray",
    }

    # Add annotations for news events
    for _, row in news_df.iterrows():
        if row["insights"]:
            for insight in row["insights"]:
                if insight["ticker"] == symbol:
                    fig.add_trace(
                        go.Scatter(
                            x=[row["published_utc"]],
                            y=[
                                (
                                    stock_df[stock_df["timestamp"] == row["published_utc"]][
                                        "close"
                                    ].values[0]
                                    if not stock_df[stock_df["timestamp"] == row["published_utc"]].empty
                                    else None
                                )
                            ],
                            mode="markers+text",
                            marker=dict(color=sentiment_colors[row["sentiment"]], size=10),
                            text=insight["sentiment_reasoning"],
                            textposition="top center",
                            name=row["title"],
                        )
                    )

    fig.show()
