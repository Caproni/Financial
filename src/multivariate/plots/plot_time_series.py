#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import plotly.graph_objects as go
from datetime import datetime
from src.utils import log


def plot_time_series(
    time_series_dict,
    title="Time-Series Plot",
    xaxis_title="Time",
    yaxis_title="Value",
    timestamps: list[datetime] = None,
):
    """
    Plot an arbitrary number of time-series using Plotly.

    Parameters:
    - time_series_dict: A dictionary where the keys are the names of the time-series, and the values are lists or arrays of the data points.
    - title: The title of the plot (default is "Time-Series Plot").
    - xaxis_title: The title of the x-axis (default is "Time").
    - yaxis_title: The title of the y-axis (default is "Value").
    - timestamps: An optional list of datetime objects for the x-axis.

    Returns:
    - fig: A Plotly figure object that can be shown or saved.
    """
    log.function_call()

    fig = go.Figure()

    for series_name, series_data in time_series_dict.items():
        if timestamps:
            x_values = timestamps
        else:
            x_values = list(range(len(series_data)))

        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=series_data,
                mode="lines",
                name=series_name,
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    # Add vertical lines for each new week if timestamps are provided
    if timestamps:
        weeks_seen = set()
        for i, timestamp in enumerate(timestamps):
            year_week = timestamp.isocalendar()[:2]  # (year, week_number)
            if year_week not in weeks_seen:
                fig.add_vline(x=timestamp, line=dict(color="black", dash="dash"))
                weeks_seen.add(year_week)

    fig.show()
