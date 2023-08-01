#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from src.utils.logger import logger as log


def calc_sharpe_ratio(
    portfolio_returns: float,
    risk_free_returns: float,
    sd_portfolio_excess_returns: float,
) -> float:
    """Calculates the Sharpe ratio

    Args:
        portfolio_returns (float): Returns of portfolio under analysis
        risk_free_returns (float): Low-risk counter-factual returns for comparison
        sd_portfolio_excess_returns (float): Standard deviation of portfolio excess returns
    """
    log.info("Calling calc_sharpe_ratio")

    return (portfolio_returns - risk_free_returns) / sd_portfolio_excess_returns
