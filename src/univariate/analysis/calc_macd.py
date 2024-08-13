#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import pandas as pd

from src.utils import log


def calc_macd(
    data: list[int | float],
    short_window: int = 12,
    long_window: int = 26,
    signal_window: int = 9,
) -> tuple[list[float], list[float], list[float], list[float]]:
    """
    Calculates the Moving Average Convergence Divergence (MACD) and its first derivative (rate of change) for the given data.

    Args:
        data: A list of integers or floats representing the price data.
        short_window: An integer specifying the short EMA window (default is 12).
        long_window: An integer specifying the long EMA window (default is 26).
        signal_window: An integer specifying the signal line window (default is 9).

    Returns:
        tuple[list[float], list[float], list[float], list[float]]: A tuple of lists containing the MACD, Signal Line, MACD Histogram, and the first derivative of the MACD Histogram.
    """
    log.function_call()

    df = pd.DataFrame({"price": data})

    df["ema_short"] = df["price"].ewm(span=short_window, adjust=False).mean()
    df["ema_long"] = df["price"].ewm(span=long_window, adjust=False).mean()

    df["macd"] = df["ema_short"] - df["ema_long"]
    df["signal_line"] = df["macd"].ewm(span=signal_window, adjust=False).mean()

    df["macd_histogram"] = df["macd"] - df["signal_line"]

    df["macd_histogram_derivative"] = df["macd_histogram"].diff()

    df = df.drop(columns=["ema_short", "ema_long", "price"])

    return (
        df["macd"].to_list(),
        df["signal_line"].to_list(),
        df["macd_histogram"].to_list(),
        df["macd_histogram_derivative"].to_list(),
    )
