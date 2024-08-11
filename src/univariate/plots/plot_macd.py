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
    timestamps: list[datetime] = None,
):
    """
    Plots the MACD, Signal Line, and MACD Histogram.

    Args:
        macd: A list of floats representing the MACD values.
        signal_line: A list of floats representing the Signal Line values.
        macd_histogram: A list of floats representing the MACD Histogram values.
        timestamps: An optional list of datetime objects representing the time points for each value.
    """

    log.function_call()

    fig = go.Figure()

    x_values = timestamps or list(range(len(macd)))
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=macd,
            mode="lines",
            name="MACD",
            line=dict(color="blue"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=signal_line,
            mode="lines",
            name="Signal Line",
            line=dict(color="orange"),
        )
    )

    fig.add_trace(
        go.Bar(
            x=x_values,
            y=macd_histogram,
            name="MACD Histogram",
            marker=dict(color="green"),
        )
    )

    # Update layout with white background
    fig.update_layout(
        title="MACD, Signal Line, and MACD Histogram",
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
