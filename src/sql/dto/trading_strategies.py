#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, UUID, String, TIMESTAMP, Float, Boolean
from ..client import Base


class TradingStrategies(Base):

    __tablename__ = "trading_strategies"

    trading_strategy_id = Column(UUID, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    universe = Column(String, nullable=False)
    valid_from = Column(TIMESTAMP, nullable=True)
    valid_to = Column(TIMESTAMP, nullable=True)
    strategy_type = Column(String, nullable=False)
    allocation_size = Column(Float, nullable=True)
    active = Column(Boolean, nullable=False)
    notes = Column(String, nullable=True)
    last_modified_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
