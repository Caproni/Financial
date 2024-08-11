#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import plotly.graph_objects as go
from datetime import datetime
from src.univariate.analysis.calc_linear_moving_average import (
    calc_linear_moving_average,
)
from src.utils import log


def plot_bollinger_bands(
    data: list[int | float],
    steps: int = 20,
    timestamps: list[datetime] = None,
):
    """Plots a time-series and Bollinger Bands for that time-series.

    Args:
        data (list[int | float]): Input time-series.
        steps (int, optional): Steps to use in calculation of moving averages. Defaults to 20.
        timestamps (list[datetime], optional): Optional list of datetime objects for the x-axis.
    """
    log.function_call()

    av, std = calc_linear_moving_average(
        data,
        steps=steps,
    )

    fig = go.Figure()

    if timestamps:
        x_values = timestamps
    else:
        x_values = list(range(len(data)))

    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=data,
            mode="lines",
            name="Price",
            line=dict(color="red"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=av,
            mode="lines",
            name="Moving Average",
            line=dict(color="blue"),
        )
    )

    upper_band = [a + 2 * s if s is not None else None for a, s in zip(av, std)]
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=upper_band,
            mode="lines",
            name="Upper Bollinger Band",
            line=dict(color="black"),
        )
    )

    lower_band = [a - 2 * s if s is not None else None for a, s in zip(av, std)]
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=lower_band,
            mode="lines",
            name="Lower Bollinger Band",
            line=dict(color="black"),
        )
    )

    fig.update_layout(
        title="Bollinger Bands",
        xaxis_title="Time",
        yaxis_title="Price",
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
