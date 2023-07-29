from alpaca.trading.client import TradingClient
from dotenv import load_dotenv


def create_client() -> TradingClient:
    load_dotenv()
    return TradingClient("api-key", "secret-key")
    print("")
