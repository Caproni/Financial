#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, UUID, String, TIMESTAMP
from ..client import Base


class StopLossCriteria(Base):

    __tablename__ = "stop_loss_criteria"

    stop_loss_criterion_id = Column(UUID, nullable=True, primary_key=True)
    criterion = Column(String, nullable=False)
    criterion_type = Column(String, nullable=False)
    last_modified_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    trading_strategy_id = Column(UUID, nullable=True)
