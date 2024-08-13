#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import plotly.graph_objects as go
from datetime import datetime
from src.utils import log


def plot_vertical_bars(
    time_series_dict,
    title="Bar Chart",
    xaxis_title="Categories",
    yaxis_title="Values",
    timestamps: list[datetime] = None,
):
    """
    Plot an arbitrary number of vertical bar charts using Plotly.

    Parameters:
    - time_series_dict: A dictionary where the keys are the names of the time-series, and the values are lists or arrays of the data points.
    - title: The title of the plot (default is "Bar Chart").
    - xaxis_title: The title of the x-axis (default is "Categories").
    - yaxis_title: The title of the y-axis (default is "Values").
    - timestamps: An optional list of datetime objects for the x-axis (not commonly used in bar charts).

    Returns:
    - fig: A Plotly figure object that can be shown or saved.
    """
    log.function_call()

    fig = go.Figure()

    for series_name, series_data in time_series_dict.items():
        x_values = timestamps or list(range(len(series_data)))
        fig.add_trace(
            go.Bar(
                x=x_values,
                y=series_data,
                name=series_name,
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        plot_bgcolor="white",
        paper_bgcolor="white",
        barmode="group",  # Group bars together for comparison
    )

    fig.show()
