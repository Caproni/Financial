#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, Integer, String, TIMESTAMP
from ..client import Base


class LiquidTickers(Base):

    __tablename__ = "liquid_tickers"

    symbol = Column(String, primary_key=True, nullable=False)
    days = Column(Integer, nullable=False)
    min_timestamp = Column(TIMESTAMP, nullable=False)
    max_timestamp = Column(TIMESTAMP, nullable=False)
    total_volume = Column(Integer, nullable=False)
