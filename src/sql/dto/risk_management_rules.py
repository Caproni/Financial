#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, UUID, String, TIMESTAMP
from ..client import Base


class RiskManagementRules(Base):

    __tablename__ = "risk_management_rules"

    risk_management_rule_id = Column(UUID, nullable=False, primary_key=True)
    rule = Column(String, nullable=False)
    rule_type = Column(String, nullable=False)
    last_modified_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    trading_strategy_id = Column(UUID, nullable=True)
