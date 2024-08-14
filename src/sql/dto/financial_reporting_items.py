#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, UUID, String, Integer, Float

from ..client import Base


class FinancialReportingItems(Base):
    """Example:

    {
        "label": "Assets",
        "order": 100,
        "unit": "USD",
        "value": 2407400000
    }
    """

    __tablename__ = "financial_reporting_items"

    financial_reporting_item_id = Column(UUID, primary_key=True, nullable=False)
    financial_id = Column(UUID, nullable=False)
    record_type = Column(String, nullable=False)
    label = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)
    value = Column(Float, nullable=False)
