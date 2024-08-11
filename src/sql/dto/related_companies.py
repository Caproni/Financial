#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, String, UUID
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
    related_company_id = Column(UUID, nullable=False)
