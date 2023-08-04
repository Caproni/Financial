#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from ...utils.logger import logger as log


def get_drawups(
    data: list[float | int],
    as_percentage: bool = True,
) -> list[float | int]:
    """Gets a list of all drawup values of a univariate timeseries.

    Args:
        data (list[float | int]): The timeseries data for which to obtain drawups.

    Returns:
        dict[str, Any]: Dictionary describing the max drawup value.
    """
    log.info("Calling get_drawups")

    drawups = []
    previous_datum = 1_000_000_000  # data values are assumed to be positive semi-definite and smaller than this number
    for i, datum in enumerate(data):
        if i + 1 < len(data) and datum < previous_datum:
            drawup = 0
            proceeding = data[i + 1 :]  # all data after the current point
            for p in proceeding:
                if p > datum and (p - datum) > drawup:
                    drawup = p - datum
                else:
                    break
            if drawup == 0:
                continue
            if as_percentage:
                drawup = drawup / datum * 100
            drawups.append(drawup)
            previous_datum = datum

    return drawups
