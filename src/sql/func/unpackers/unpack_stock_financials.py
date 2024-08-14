#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from uuid import uuid4

from src.sql.dto import FinancialReportingItems, Financials
from src.utils import log


def unpack_stock_financials(
    data: list[dict[str, Any]]
) -> tuple[list[FinancialReportingItems], list[Financials]]:

    log.function_call()

    financial_documents: list[Financials] = []
    financial_reporting_item_documents: list[FinancialReportingItems] = []
    for datum in data:
        if datum is not None:
            financial_id = str(uuid4())
            financial_documents.append(
                Financials(
                    financial_id=financial_id,
                    cik=datum["cik"],
                    company_name=datum["company_name"],
                    end_date=datum["end_date"],
                    filing_date=datum["filing_date"],
                    fiscal_period=datum["fiscal_period"],
                    fiscal_year=datum["fiscal_year"],
                    source_filing_file_url=datum["source_filing_file_url"],
                    source_filing_url=datum["source_filing_url"],
                    start_date=datum["start_date"],
                    ticker=datum["ticker"],
                )
            )
            for e in datum["financials"]:
                financial_reporting_item_documents.append(
                    FinancialReportingItems(
                        financial_reporting_item_id=str(uuid4()),
                        financial_id=financial_id,
                        record_type=e["record_type"],
                        label=e["label"],
                        order=e["order"],
                        unit=e["unit"],
                        value=e["value"],
                    )
                )

    return financial_reporting_item_documents, financial_documents
