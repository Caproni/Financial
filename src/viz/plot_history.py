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
    collection: str,
    news_flag: bool = False,
    news_item_alignment: str | None = None,
):
    """
    Plots historical stock data with optional news annotations.

    Args:
        mongo_client: MongoClient instance for database connection.
        symbol: Stock symbol for which data is plotted.
        collection: Name of the collection in the database.
        news_flag: Flag to include news annotations (default is False).
        news_item_alignment: Alignment for news items, either 'D' (day) or 'H' (hour).

    Returns:
        None

    Raises:
        AssertionError: If news_item_alignment is not 'D' or 'H'.
    """
    log.function_call()

    if news_item_alignment is None:
        news_item_alignment = "D"

    assert news_item_alignment in {
        "D",
        "H",
    }, "News item alignment should be one of D (day), H (hour)."

    stocks = get_data(
        mongo_client,
        database="financial",
        collection=collection,
        pipeline=[{"$match": {"symbol": symbol}}],
    )

    if not stocks:
        log.warning(f"No stock data available for selected symbol: {symbol}")
        return None

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

    log.info("Constructing plot.")

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
        legend={
            "yanchor": "top",
            "y": 1,
            "xanchor": "left",
            "x": 1,
            "font": {"size": 12},
            "title": "Publications",
            "traceorder": "normal",
            "itemwidth": 30,  # This controls the width of each legend item
            "itemsizing": "constant",  # Ensures items have the same width
        },
        updatemenus=[
            {
                "type": "buttons",
                "direction": "left",
                "buttons": [
                    dict(
                        args=["showlegend", False],
                        label="Hide Legend",
                        method="relayout",
                    ),
                    dict(
                        args=["showlegend", True],
                        label="Show Legend",
                        method="relayout",
                    ),
                ],
                "pad": {"r": 10, "t": 10},
                "showactive": True,
                "x": 1.0,
                "xanchor": "left",
                "y": 0.15,
                "yanchor": "top",
            },
        ],
        margin={"t": 50},
    )

    sentiment_colors = {
        "positive": "green",
        "negative": "red",
        "bearish": "red",
        "neutral": "gray",
    }

    # Add annotations for news events
    for _, row in news_df.iterrows():
        log.info(f"Processing news article: {row['title']}")
        rounded_timestamp = row["published_utc"].round(news_item_alignment)
        stocks_df["time_diff"] = (stocks_df["timestamp"] - row["published_utc"]).abs()
        nearest_row = stocks_df.loc[stocks_df["time_diff"].idxmin()]
        stocks_df.drop(columns=["time_diff"], inplace=True)
        linked_stocks_df = nearest_row.to_frame().T
        if row["insights"]:
            log.info("Insights found.")
            for insight in row["insights"]:
                if insight["ticker"] == symbol:
                    log.info("Matched symbol.")

                    fig.add_trace(
                        go.Scatter(
                            x=[rounded_timestamp],
                            y=[
                                (
                                    None
                                    if linked_stocks_df.empty
                                    else linked_stocks_df["close"].values[0]
                                )
                            ],
                            mode="markers+text",
                            marker=dict(
                                color=sentiment_colors[insight["sentiment"]],
                                size=10,
                            ),
                            hovertext=row["title"],
                            hoverinfo="text",
                            textposition="top center",
                            name=row["title"] + f" ({row['published_utc']})",
                        )
                    )
                    break
        else:
            log.info("No insights found.")
            fig.add_trace(
                go.Scatter(
                    x=[rounded_timestamp],
                    y=[
                        (
                            None
                            if linked_stocks_df.empty
                            else linked_stocks_df["close"].values[0]
                        )
                    ],
                    mode="markers+text",
                    marker=dict(
                        color=sentiment_colors["neutral"],
                        size=10,
                    ),
                    hovertext=row["title"],
                    hoverinfo="text",
                    textposition="top center",
                    name=row["title"] + f" ({row['published_utc']})",
                )
            )

    fig.update_layout(
        xaxis=dict(fixedrange=False),  # Allow zoom on the x-axis
        yaxis=dict(fixedrange=False),  # Allow zoom on the y-axis
    )

    fig.show()
