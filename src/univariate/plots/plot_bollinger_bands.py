#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

import matplotlib.pyplot as plt

from ..analysis.get_moving_average import get_moving_average
from ...utils.logger import logger as log


def plot_bollinger_bands(
    data: list[int | float],
    weighting: str = "linear",
    steps: int = 20,
):
    log.info("Calling plot_bollinger_bands")
    
    av, std = get_moving_average(
        data, 
        weighting=weighting,
        steps=steps,
    )
    
    plt.plot(data, c="r")
    plt.plot(av, c="b")
    plt.plot([a + 2 * s if s is not None else None for a, s in zip(av, std)], c="k")
    plt.plot([a - 2 * s if s is not None else None for a, s in zip(av, std)], c="k")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.show()
    