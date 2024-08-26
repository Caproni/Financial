#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, UUID, String, TIMESTAMP
from ..client import Base


class EntryCriteria(Base):

    __tablename__ = "entry_criteria"

    entry_criterion_id = Column(UUID, nullable=False, primary_key=True)
    criterion = Column(String, nullable=False)
    criterion_type = Column(String, nullable=False)
    last_modified_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    trading_strategy_id = Column(UUID, nullable=True)
