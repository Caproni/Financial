#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import plotly.graph_objects as go
from src.utils import log


def plot_histogram(
    time_series_dict,
    title="Histogram",
    xaxis_title="Values",
    yaxis_title="Count",
):
    """
    Plot an arbitrary number of histograms using Plotly.

    Parameters:
    - time_series_dict: A dictionary where the keys are the names of the time-series, and the values are lists or arrays of the data points.
    - title: The title of the plot (default is "Histogram").
    - xaxis_title: The title of the x-axis (default is "Values").
    - yaxis_title: The title of the y-axis (default is "Count").
    - timestamps: An optional list of datetime objects for the x-axis (not used for histogram).

    Returns:
    - fig: A Plotly figure object that can be shown or saved.
    """
    log.function_call()

    fig = go.Figure()

    for series_name, series_data in time_series_dict.items():
        fig.add_trace(
            go.Histogram(
                x=series_data,
                name=series_name,
                opacity=0.75,  # Adjust opacity for overlap visualization
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        plot_bgcolor="white",
        paper_bgcolor="white",
        barmode="overlay",  # Overlay histograms for better comparison
    )

    fig.show()