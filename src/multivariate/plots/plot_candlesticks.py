#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

from src.utils import log


def plot_candlesticks(
    tickers_data: dict[str, dict[str, list[float | int | datetime]]]
):
    """
    Plot candlestick charts for multiple stock tickers using Plotly.

    Parameters:
    tickers_data (dict): A dictionary where the key is the ticker name, and the value is a dictionary
    containing the 'Datetime', 'Open', 'High', 'Low', and 'Close' data.

    Example of tickers_data structure:
    {
        'AAPL': {
            'Datetime': [datetime1, datetime2, ...],
            'Open': [open1, open2, ...],
            'High': [high1, high2, ...],
            'Low': [low1, low2, ...],
            'Close': [close1, close2, ...],
        },
        'MSFT': {
            'Datetime': [datetime1, datetime2, ...],
            'Open': [open1, open2, ...],
            'High': [high1, high2, ...],
            'Low': [low1, low2, ...],
            'Close': [close1, close2, ...],
        }
    }
    """
    log.function_call()

    num_tickers = len(tickers_data)

    # Create a subplot figure with a candlestick chart for each ticker
    fig = make_subplots(
        rows=num_tickers,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        subplot_titles=list(tickers_data.keys()),
    )

    for i, (ticker, data) in enumerate(tickers_data.items(), start=1):
        fig.add_trace(
            go.Candlestick(
                x=data['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name=ticker
            ),
            row=i, col=1
        )

    fig.update_layout(
        title=f"Candlestick Charts for: {", ".join(tickers_data.keys())}",
        xaxis_title="Datetime",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        height=300 * num_tickers
    )

    fig.show()
