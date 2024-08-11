#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, Boolean, Integer, String, TIMESTAMP, Float, UUID
from ..client import Base


class PolygonMarketDataHour(Base):
    """Example:

    {
        "symbol": "OILY",
        "open": 1.25,
        "high": 1.45,
        "low": 1.15,
        "close": 1.18,
        "otc": True,
        "timestamp": "2019-05-07 15:00:00",
        "transactions": 1,
        "volume": 8000,
        "vwap": 1.25
    }
    """

    __tablename__ = "polygon_market_data_hour"

    symbol = Column(String, nullable=True, primary_key=True)
    otc = Column(Boolean, nullable=True)
    timestamp = Column(TIMESTAMP(timezone=False), nullable=False, primary_key=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    transactions = Column(Integer, nullable=True)
    volume = Column(Integer, nullable=True)
    vwap = Column(Float, nullable=True)
    data_id = Column(UUID, nullable=False)
