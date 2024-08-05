#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

import matplotlib.pyplot as plt
from math import sqrt, floor

from ..analysis.get_drawdowns import get_drawdowns
from src.utils import log


def plot_drawdown_histogram(
    data: list[int | float],
):
    log.function_call()

    drawdowns = get_drawdowns(data)

    plt.hist(
        drawdowns,
        bins=floor(sqrt(len(drawdowns))),
    )
    plt.xlabel("Drawdown")
    plt.ylabel("Frequency")
    plt.show()
