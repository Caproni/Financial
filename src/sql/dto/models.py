#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, UUID, String, TIMESTAMP, Float, Integer
from ..client import Base


class Models(Base):

    __tablename__ = "models"

    model_id = Column(UUID, nullable=False, primary_key=True)
    model_url = Column(String, nullable=False)
    symbols = Column(String, nullable=False)
    features = Column(String, nullable=False)
    confusion_matrix = Column(String, nullable=False)
    classification_report = Column(String, nullable=False)
    training_set_rows = Column(Integer, nullable=False)
    training_data_url = Column(String, nullable=False)
    training_targets_url = Column(String, nullable=False)
    test_set_rows = Column(Integer, nullable=False)
    test_data_url = Column(String, nullable=False)
    test_targets_url = Column(String, nullable=False)
    serving_set_rows = Column(Integer, nullable=False)
    serving_data_url = Column(String, nullable=False)
    serving_targets_url = Column(String, nullable=False)
    accuracy = Column(Float, nullable=False)
    balanced_accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    y_serve = Column(String, nullable=False)
    y_serve_pred = Column(String, nullable=False)
    serving_set_indicated_entry_prices = Column(String, nullable=False)
    serving_set_indicated_exit_prices = Column(String, nullable=False)
    last_modified_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
