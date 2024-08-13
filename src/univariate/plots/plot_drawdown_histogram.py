#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os.path import abspath, join, dirname
import plotly.graph_objects as go
import plotly.offline as pyo
from math import sqrt, floor

from ..analysis.get_drawdowns import get_drawdowns
from src.utils import log


def plot_drawdown_histogram(
    data: list[int | float],
    title: str = "Drawdown Histogram",
) -> str:
    """Plots a histogram of drawdown values for a time-series.

    Args:
        data (list[int | float]): Input time-series.
        title: (str, optional): Title and filename for saved html file.

    Returns:
        Path to a generated html file containing the plot.
    """
    log.function_call()

    drawdowns = get_drawdowns(data)

    num_bins = floor(sqrt(len(drawdowns)))

    fig = go.Figure(data=[go.Histogram(x=drawdowns, nbinsx=num_bins)])

    fig.update_layout(
        title=title,
        xaxis_title="Drawdown",
        yaxis_title="Frequency",
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    path_to_output = abspath(
        join(dirname(__file__), "../../../staging", f"{title}.html")
    )
    pyo.plot(
        fig,
        filename=path_to_output,
        auto_open=True,
    )
    return path_to_output
