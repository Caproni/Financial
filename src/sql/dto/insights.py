#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, UUID, String
from ..client import Base


class Insights(Base):

    __tablename__ = "insights"

    insight_id = Column(UUID, nullable=False, primary_key=True)
    sentiment = Column(String, nullable=False)
    sentiment_reasoning = Column(String, nullable=False)
    ticker = Column(String, nullable=False, primary_key=True)

