#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from src.utils.logger import logger as log


def calc_kelly_bet(
    p_win: float,
    win_loss_ratio: float,
) -> float:
    """Calculates the Kelly bet

    Args:
        p_win (float): Probability of a deal being profitable
        win_loss_ratio (float): Sum of profits divided by sum of losses
    """
    log.info("Calling calc_kelly_bet")

    return p_win - (1 - p_win) / win_loss_ratio
