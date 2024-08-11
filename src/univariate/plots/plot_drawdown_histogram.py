#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import plotly.graph_objects as go
from math import sqrt, floor
from datetime import datetime

from ..analysis.get_drawdowns import get_drawdowns
from src.utils import log


def plot_drawdown_histogram(
    data: list[int | float],
):
    log.function_call()

    drawdowns = get_drawdowns(data)

    num_bins = floor(sqrt(len(drawdowns)))

    fig = go.Figure(data=[go.Histogram(x=drawdowns, nbinsx=num_bins)])

    fig.update_layout(
        title="Drawdown Histogram",
        xaxis_title="Drawdown",
        yaxis_title="Frequency",
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    fig.show()
