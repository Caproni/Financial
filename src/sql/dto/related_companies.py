#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, Boolean, String
from ..client import Base


class RelatedCompanies(Base):
    """Example:

    {
        "symbol": "A",
        "ticker": "B",
    }
    """

    __tablename__ = "related_companies"

    symbol = Column(String, primary_key=True, nullable=False)
    ticker = Column(String, primary_key=True, nullable=False)
