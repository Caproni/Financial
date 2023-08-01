from alpaca.trading.client import TradingClient
from dotenv import load_dotenv
from os import getenv

from src.utils.logger import logger as log


def create_trading_client(
    paper: bool = True,
) -> TradingClient:
    log.info("Calling create_trading_client")
    load_dotenv()
    return TradingClient(
        getenv("ALPACA_PAPER_KEY") if paper else getenv("ALPACA_LIVE_KEY"),
        getenv("ALPACA_PAPER_SECRET") if paper else getenv("ALPACA_LIVE_SECRET"),
        paper=paper,
    )
