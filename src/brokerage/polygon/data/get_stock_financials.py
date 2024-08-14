#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from copy import deepcopy
from polygon import RESTClient
from datetime import datetime

from src.utils import log


def get_stock_financials(
    client: RESTClient,
    ticker: str,
) -> list[dict[str, Any]]:
    """Gets fundamental stock financial data from Polygon.io.

    Args:
        client (RESTClient): A Polygon client.
        ticker (str): A specific ticker / symbol.

    Returns:
        list[dict[str, Any]]: A list of dictionaries representing financial data.
    """
    log.function_call()

    try:
        responses = client.vx.list_stock_financials(
            ticker=ticker,
            limit=100,
        )
    except Exception as e:
        log.error(f"Error: {e}")
        raise e

    financials: list[dict[str, Any]] = []
    for e in responses:
        financial_reporting_items: list[dict[str, Any]] = []

        if e.financials.balance_sheet is not None:
            for v in e.financials.balance_sheet.values():
                if v is not None:
                    financial_reporting_items.append(
                        {
                            "record_type": "balance_sheet",
                            "label": v.label,
                            "order": v.order,
                            "unit": v.unit,
                            "value": v.value,
                        }
                    )

        if e.financials.cash_flow_statement is not None:
            for v in [
                e.financials.cash_flow_statement.net_cash_flow,
                e.financials.cash_flow_statement.net_cash_flow_from_financing_activities,
            ]:
                if v is not None:
                    financial_reporting_items.append(
                        {
                            "record_type": "cash_flow_statement",
                            "label": v.label,
                            "order": v.order,
                            "unit": v.unit,
                            "value": v.value,
                        }
                    )

        if e.financials.comprehensive_income is not None:
            for v in [
                e.financials.comprehensive_income.comprehensive_income_loss,
                e.financials.comprehensive_income.comprehensive_income_loss_attributable_to_parent,
                e.financials.comprehensive_income.other_comprehensive_income_loss,
            ]:
                if v is not None:
                    financial_reporting_items.append(
                        {
                            "record_type": "comprehensive_income",
                            "label": v.label,
                            "order": v.order,
                            "unit": v.unit,
                            "value": v.value,
                        }
                    )

        if e.financials.comprehensive_income is not None:
            for v in [
                e.financials.income_statement.operating_expenses,
                e.financials.income_statement.revenues,
                e.financials.income_statement.gross_profit,
                e.financials.income_statement.cost_of_revenue,
                e.financials.income_statement.basic_earnings_per_share,
            ]:
                if v is not None:
                    financial_reporting_items.append(
                        {
                            "record_type": "income_statement",
                            "label": v.label,
                            "order": v.order,
                            "unit": v.unit,
                            "value": v.value,
                        }
                    )
        
        financials.append(
            {
                "ticker": ticker,
                "cik": e.cik,
                "company_name": e.company_name,
                "end_date": datetime.fromisoformat(e.end_date),
                "filing_date": (
                    datetime.fromisoformat(e.filing_date)
                    if e.filing_date is not None
                    else None
                ),
                "financials": deepcopy(financial_reporting_items),
                "fiscal_period": e.fiscal_period,
                "fiscal_year": e.fiscal_year,
                "source_filing_file_url": e.source_filing_file_url,
                "source_filing_url": e.source_filing_url,
                "start_date": datetime.fromisoformat(e.start_date),
            }
        )

    return financials
