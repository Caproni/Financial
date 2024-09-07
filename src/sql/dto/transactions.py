#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, Boolean, String, UUID, DATETIME, Float, TIMESTAMP
from ..client import Base


class Transactions(Base):
    """Example:

    {
        "transaction_id": "f282addd-7b7d-4563-958e-6511b29d8694",
        "description": "Buy 10 AAPL Market Order",
        "placed_timestamp": "2024-03-04 14:00:07.123"
        "accepted_timestamp": "2024-03-04 14:00:07.179",
        "order_type": "MARKET",
        "side": "BUY",
        "value": 123.04,
        "currency": "USD",
        "quantity": 10.0,
        "ticker": "AAPL",
        "exchange": "NASDAQ",
        "broker": "Alpaca",
        "paper": true,
        "backtest": false,
        "live": false,
    }
    """

    __tablename__ = "transactions"

    transaction_id = Column(UUID, nullable=False, primary_key=True)
    description = Column(String, nullable=False)
    placed_timestamp = Column(DATETIME, nullable=False)
    accepted_timestamp = Column(DATETIME, nullable=True)
    order_type = Column(String, nullable=False)
    side = Column(String, nullable=False)
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)
    currency = Column(String, nullable=True)
    quantity = Column(Float, nullable=False)
    ticker = Column(String, nullable=False)
    exchange = Column(String, nullable=True)
    broker = Column(String, nullable=False)
    paper = Column(Boolean, nullable=False)
    backtest = Column(Boolean, nullable=False)
    live = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    last_modified_at = Column(TIMESTAMP, nullable=False)
    model_id = Column(UUID, nullable=True)
