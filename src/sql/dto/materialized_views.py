#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, String, TIMESTAMP
from ..client import Base


class MaterializedViews(Base):

    __tablename__ = "materialized_views"

    materialized_view_name = Column(String, nullable=False, primary_key=True)
    last_refreshed = Column(TIMESTAMP, nullable=False)
