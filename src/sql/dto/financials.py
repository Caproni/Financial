#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, UUID, String, TIMESTAMP
from ..client import Base


class Financials(Base):
    """Example:

    {
        "cik": "0001650729",
        "company_name": "SiteOne Landscape Supply, Inc.",
        "end_date": "2022-04-03",
        "filing_date": "2022-05-04",
        "fiscal_period": "Q1",
        "fiscal_year": "2022",
        "source_filing_file_url": "https://api.polygon.io/v1/reference/sec/filings/0001650729-22-000010/files/site-20220403_htm.xml",
        "source_filing_url": "https://api.polygon.io/v1/reference/sec/filings/0001650729-22-000010",
        "start_date": "2022-01-03"
    }
    """

    __tablename__ = "financials"

    financial_id = Column(UUID, primary_key=True, nullable=False)
    cik = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)
    filing_date = Column(TIMESTAMP, nullable=True)
    fiscal_period = Column(String, nullable=False)
    fiscal_year = Column(String, nullable=False)
    source_filing_file_url = Column(String, nullable=True)
    source_filing_url = Column(String, nullable=True)
    start_date = Column(TIMESTAMP, nullable=False)
    ticker = Column(String, nullable=False)
