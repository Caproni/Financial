#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, UUID, String, TIMESTAMP, Float, Integer
from ..client import Base


class ModelProfitAnalysis(Base):

    __tablename__ = "model_profit_analysis"

    model_id = Column(UUID, nullable=False, primary_key=True)
    symbol = Column(String, nullable=False)
    training_set_rows = Column(Integer, nullable=False)
    test_set_rows = Column(Integer, nullable=False)
    serving_set_rows = Column(Integer, nullable=False)
    accuracy = Column(Float, nullable=False)
    balanced_accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    total_profit_or_loss = Column(Float, nullable=False)
    variance_daily_profit_or_loss = Column(Float, nullable=False)
    sd_daily_profit_or_loss = Column(Float, nullable=False)
    daily_average_profit_or_loss = Column(Float, nullable=False)
    max_daily_profit_or_loss = Column(Float, nullable=False)
    min_daily_profit_or_loss = Column(Float, nullable=False)
    last_modified_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
