#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

import matplotlib.pyplot as plt
from math import sqrt

from ..analysis.get_drawdowns import get_drawdowns
from src.utils.logger import logger as log


def plot_drawdown_histogram(
    data: list[int | float],
) -> plt.figure:
    log.info("Calling plot_drawdown_histogram")

    drawdowns = get_drawdowns(data)

    fig = plt.figure()
    fig.hist(
        drawdowns,
        bins=sqrt(len(drawdowns)),
    )
    return fig
