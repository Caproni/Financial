#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from src.sql import (
    get_data,
    TradingStrategies,
    ExitCriteria,
    EntryCriteria,
    StopLossCriteria,
    RiskManagementRules,
    TakeProfitCriteria,
)
from src.utils import log


def get_strategies():
    log.function_call()

    get_data()
