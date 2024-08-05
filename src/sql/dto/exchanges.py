#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, Integer, String
from ..client import Base


class Exchanges(Base):
    """Example:

    {
        "id": 1,
        "type": "exchange",
        "asset_class": "stocks",
        "locale": "us",
        "name": "NYSE American, LLC",
        "acronym": "AMEX",
        "mic": "XASE",
        "operating_mic": "XNYS",
        "participant_id": "A",
        "url": "https://www.nyse.com/markets/nyse-american"
    }
    """

    __tablename__ = "exchanges"

    id = Column(Integer, nullable=True)
    type = Column(String, nullable=False)
    asset_class = Column(String, nullable=False)
    locale = Column(String, nullable=False)
    name = Column(String, nullable=False, primary_key=True)
    acronym = Column(String, nullable=True)
    mic = Column(String, nullable=True)
    operating_mic = Column(String, nullable=True)
    participant_id = Column(String, nullable=True)
    url = Column(String, nullable=True)
