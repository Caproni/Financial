#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import plotly.graph_objects as go
from datetime import datetime
from src.utils import log


def plot_macd(
    macd: list[float],
    signal_line: list[float],
    macd_histogram: list[float],
    macd_histogram_derivative: list[float],
    timestamps: list[datetime] = None,
):
    """
    Plots the MACD, Signal Line, MACD Histogram, and the first derivative of the MACD Histogram.

    Args:
        macd: A list of floats representing the MACD values.
        signal_line: A list of floats representing the Signal Line values.
        macd_histogram: A list of floats representing the MACD Histogram values.
        macd_histogram_derivative: A list of floats representing the first derivative of the MACD Histogram values.
        timestamps: An optional list of datetime objects representing the time points for each value.
    """

    log.function_call()

    fig = go.Figure()

    x_values = timestamps or list(range(len(macd)))
    
    # Plot MACD line
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=macd,
            mode="lines",
            name="MACD",
            line=dict(color="blue"),
        )
    )

    # Plot Signal Line
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=signal_line,
            mode="lines",
            name="Signal Line",
            line=dict(color="orange"),
        )
    )

    # Plot MACD Histogram as bars
    fig.add_trace(
        go.Bar(
            x=x_values,
            y=macd_histogram,
            name="MACD Histogram",
            marker=dict(color="green"),
        )
    )

    # Plot the first derivative of the MACD Histogram as a line
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=macd_histogram_derivative,
            mode="lines",
            name="MACD Histogram Derivative",
            line=dict(color="red", dash="dot"),
        )
    )

    # Update layout with white background
    fig.update_layout(
        title="MACD, Signal Line, MACD Histogram, and MACD Histogram Derivative",
        xaxis_title="Time",
        yaxis_title="Value",
        legend_title="Legend",
        barmode="relative",
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    # Add vertical lines for each new week if timestamps are provided
    if timestamps:
        weeks_seen = set()
        for timestamp in timestamps:
            year_week = timestamp.isocalendar()[:2]  # (year, week_number)
            if year_week not in weeks_seen:
                fig.add_vline(x=timestamp, line=dict(color="black", dash="dash"))
                weeks_seen.add(year_week)

    fig.show()