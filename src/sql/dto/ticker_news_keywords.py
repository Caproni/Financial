#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, UUID, String
from ..client import Base


class TickerNewsKeywords(Base):

    __tablename__ = "ticker_news_keywords"

    keyword_id = Column(UUID, nullable=False, primary_key=True)
    keyword = Column(String, nullable=False, primary_key=True)
