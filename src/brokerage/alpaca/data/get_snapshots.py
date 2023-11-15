#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockSnapshotRequest
from alpaca.data.models import Snapshot

from src.utils import log


def get_snapshots(
    historical_stock_client: StockHistoricalDataClient,
    symbols: list[str],
) -> dict[str, Snapshot]:
    """Gets a snapshot of the requested stocks

    Args:
        historical_stock_client (StockHistoricalDataClient): An Alpaca historical stock data client
        symbols (list[str]): A list of symbols for which to obtain data

    Returns:
        dict[str, Snapshot]: A dictionary of snapshots
    """
    log.info("Calling get_snapshots")

    pagination_limit = 20
    current = 0
    snapshots: dict[str, Snapshot] = {}
    while current < len(symbols):
        data = {}
        try:
            data = historical_stock_client.get_stock_snapshot(
                StockSnapshotRequest(
                    symbol_or_symbols=[
                        s.replace("/", "")
                        for s in symbols[
                            current : min(current + pagination_limit, len(symbols))
                        ]
                    ]
                )
            )
        except Exception as e:
            err_symbols = [
                s.replace("/", "")
                for s in symbols[
                    current : min(current + pagination_limit, len(symbols))
                ]
            ]
            log.info(f"Could not obtain data for {err_symbols}. Error: {e}")
            for err_sym in err_symbols:
                try:
                    individual_snapshot = historical_stock_client.get_stock_snapshot(
                        StockSnapshotRequest(symbol_or_symbols=[err_sym])
                    )
                    data.update(individual_snapshot)
                except Exception as e:
                    log.warning(f"Could not obtain data for {err_sym}. Error: {e}")

        snapshots.update(data)
        current = min(current + pagination_limit, len(symbols))

    return snapshots
