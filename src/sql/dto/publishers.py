#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, UUID, String
from ..client import Base


class Publishers(Base):

    __tablename__ = "publishers"

    publisher_id = Column(UUID, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    homepage_url = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    favicon_url = Column(String, nullable=True)

