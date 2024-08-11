#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, Boolean, String, UUID
from ..client import Base


class Tickers(Base):
    """Example:

    {
        "ticker": "A",
        "name": "Agilent Technologies Inc.",
        "market": "stocks",
        "locale": "us",
        "primary_exchange": "XNYS",
        "type": "CS",
        "active": true,
        "currency_name": "usd",
        "cik": "0001090872",
        "composite_figi": "BBG000C2V3D6",
        "share_class_figi": "BBG001SCTQY4",
        "last_updated_utc": "2024-05-17T00:00:00Z"
    }
    """

    __tablename__ = "tickers"

    ticker = Column(String, nullable=False)
    name = Column(String, primary_key=True, nullable=True)
    market = Column(String, nullable=False)
    locale = Column(String, nullable=False)
    primary_exchange = Column(String, nullable=True)
    type = Column(String, nullable=True)
    active = Column(Boolean, nullable=False)
    currency_name = Column(String, nullable=True)
    cik = Column(String, nullable=True)
    composite_figi = Column(String, nullable=True)
    share_class_figi = Column(String, nullable=True)
    last_updated_utc = Column(String, nullable=True)
    ticker_id = Column(UUID, nullable=False)
